"""Thin LLM client over Groq with retries, rate-limit backoff, JSON parsing and
model fallback. Every call is tagged with a `role` (planner / generator /
judge / learner / distiller) so token usage can be traced per agent."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field

from . import config


class LLMError(RuntimeError):
    pass


@dataclass
class Usage:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    by_role: dict = field(default_factory=dict)

    def add(self, role: str, p: int, c: int) -> None:
        self.calls += 1
        self.prompt_tokens += p
        self.completion_tokens += c
        r = self.by_role.setdefault(role, {"calls": 0, "tokens": 0})
        r["calls"] += 1
        r["tokens"] += p + c


def extract_json(text: str) -> dict:
    """Parse JSON even if the model wrapped it in ``` fences or added prose."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fenced:
        return json.loads(fenced.group(1))
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise LLMError(f"Model did not return JSON: {text[:300]}")


class GroqLLM:
    def __init__(self, api_key: str | None = None):
        from groq import Groq  # imported lazily so the mock mode needs no key

        key = api_key or config.GROQ_API_KEY
        if not key:
            raise LLMError("GROQ_API_KEY is missing. Put it in the .env file (see README).")
        self.client = Groq(api_key=key)
        self.usage = Usage()
        self._dead_models: set[str] = set()
        self._no_extra: set[str] = set()
        self.resolve_models()

    # ------------------------------------------------------ model choice ---
    def available_models(self) -> list[str]:
        try:
            return sorted(m.id for m in self.client.models.list().data if _is_chat_model(m.id))
        except Exception as e:
            print(f"   [could not list models: {e}]")
            return []

    def resolve_models(self) -> None:
        """Groq retires models often. Ask the API which chat models this key can
        use, keep the configured ones if available, else pick the best match
        from a preference list. Generator and evaluator are kept DIFFERENT."""
        avail = self.available_models()
        if not avail:
            return
        def pick(wanted, prefs, avoid=None):
            if wanted in avail and wanted != avoid:
                return wanted
            for p in prefs:  # exact id first, then substring match (ids change between versions)
                hits = [m for m in avail if m == p] or [m for m in avail if p in m.lower()]
                hits = [m for m in hits if m != avoid]
                if hits:
                    return sorted(hits)[-1]
            others = [m for m in avail if m != avoid]
            return (others or avail)[0]
        gen = pick(config.GENERATOR_MODEL, GENERATOR_PREFS)
        ev = pick(config.EVALUATOR_MODEL, EVALUATOR_PREFS, avoid=gen)
        lr = pick(config.LEARNER_MODEL, LEARNER_PREFS, avoid=gen)
        fb = pick(config.FALLBACK_MODEL, FALLBACK_PREFS, avoid=None)
        for name, old, new in (("generator", config.GENERATOR_MODEL, gen), ("evaluator", config.EVALUATOR_MODEL, ev),
                               ("learner", config.LEARNER_MODEL, lr), ("fallback", config.FALLBACK_MODEL, fb)):
            if old != new:
                why = "kept different from the generator" if (name == "evaluator" and old == gen) else "resolved"
                print(f"   [models] {name}: '{old}' -> '{new}' ({why})")
        config.GENERATOR_MODEL, config.EVALUATOR_MODEL, config.LEARNER_MODEL, config.FALLBACK_MODEL = gen, ev, lr, fb

    def _call(self, model, messages, temperature, json_mode, max_tokens, role):
        kwargs = dict(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        extra = {}
        if model not in self._no_extra:
            if "gpt-oss" in model:
                extra = {"reasoning_effort": "medium"}
                kwargs["max_tokens"] = max(max_tokens, 8000)   # reasoning tokens count toward the limit
            elif "qwen" in model:
                extra = {"reasoning_format": "hidden"}
                kwargs["max_tokens"] = max(max_tokens, 8000)
        try:
            resp = self.client.chat.completions.create(**kwargs, **extra)
        except Exception as e:
            if extra and getattr(e, "status_code", None) == 400 and any(k in str(e) for k in extra):
                self._no_extra.add(model)  # this model does not accept the reasoning param
                resp = self.client.chat.completions.create(**kwargs)
            else:
                raise
        u = resp.usage
        self.usage.add(role, getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0)
        text = resp.choices[0].message.content or ""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()  # reasoning models

    def chat(self, system: str, user: str, *, model: str, temperature: float = 0.3,
             json_mode: bool = False, max_tokens: int = 4096, role: str = "llm") -> str:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        candidates = [m for m in dict.fromkeys((model, config.FALLBACK_MODEL)) if m not in self._dead_models]
        if not candidates:
            raise LLMError(f"No usable model left (tried {model}, {config.FALLBACK_MODEL}). "
                           "Run `python main.py models` and set GENERATOR_MODEL / EVALUATOR_MODEL in .env.")
        last_err: Exception | None = None
        for m in candidates:
            for attempt in range(5):
                try:
                    return self._call(m, messages, temperature, json_mode, max_tokens, role)
                except Exception as e:  # groq raises typed errors; keep this dependency-light
                    last_err = e
                    msg = str(e).lower()
                    status = getattr(e, "status_code", None)
                    if status == 429 or "rate limit" in msg or "rate_limit" in msg:
                        wait = _retry_after_seconds(msg) or min(60, 5 * (attempt + 1))
                        print(f"   [rate limit on {m}] waiting {wait:.0f}s ...")
                        time.sleep(wait)
                        continue
                    if status in (400, 404) and ("model" in msg and ("not found" in msg or "decommissioned" in msg or "does not exist" in msg)):
                        print(f"   [model {m} unavailable, falling back]")
                        self._dead_models.add(m)
                        break
                    if json_mode and status == 400 and "json" in msg:
                        # model failed to produce valid JSON; retry once without JSON mode
                        json_mode = False
                        continue
                    if status and status >= 500:
                        time.sleep(3 * (attempt + 1))
                        continue
                    raise LLMError(str(e)) from e
        raise LLMError(f"All model attempts failed: {last_err}")

    def chat_json(self, system: str, user: str, **kw) -> dict:
        raw = self.chat(system, user, json_mode=True, **kw)
        try:
            return extract_json(raw)
        except Exception:
            # one repair attempt
            fixed = self.chat("Return ONLY valid JSON. No prose.",
                              f"Fix this into valid JSON with the same content:\n{raw}",
                              json_mode=True, model=kw.get("model", config.EVALUATOR_MODEL),
                              temperature=0, role=kw.get("role", "llm") + "-repair")
            return extract_json(fixed)


GENERATOR_PREFS = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "meta-llama/llama-4-maverick-17b-128e-instruct", "moonshotai/kimi-k2-instruct",
                   "moonshotai/kimi-k2-instruct-0905", "openai/gpt-oss-120b", "qwen/qwen3-32b",
                   "meta-llama/llama-4-scout-17b-16e-instruct", "openai/gpt-oss-20b", "llama-3.1-8b-instant"]
EVALUATOR_PREFS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "moonshotai/kimi-k2-instruct-0905", "moonshotai/kimi-k2-instruct", "qwen/qwen3-32b",
                   "meta-llama/llama-4-maverick-17b-128e-instruct", "llama-3.3-70b-versatile", "openai/gpt-oss-20b"]
LEARNER_PREFS = ["qwen", "llama", "kimi", "openai/gpt-oss-20b"]
FALLBACK_PREFS = ["openai/gpt-oss-20b", "gpt-oss-20b", "llama-3.1-8b-instant", "meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b"]
_NON_CHAT = ("whisper", "tts", "guard", "orpheus", "playai", "distil", "embed", "compound", "allam", "safeguard")


def _is_chat_model(mid: str) -> bool:
    return not any(x in mid.lower() for x in _NON_CHAT)


def _retry_after_seconds(msg: str) -> float | None:
    m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", msg)
    if m:
        return (int(m.group(1) or 0) * 60) + float(m.group(2)) + 1
    return None


def get_llm(mock: bool = False):
    if mock:
        from .mock_llm import MockLLM
        return MockLLM()
    return GroqLLM()
