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

    def _call(self, model, messages, temperature, json_mode, max_tokens, role):
        kwargs = dict(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        resp = self.client.chat.completions.create(**kwargs)
        u = resp.usage
        self.usage.add(role, getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0)
        return resp.choices[0].message.content or ""

    def chat(self, system: str, user: str, *, model: str, temperature: float = 0.3,
             json_mode: bool = False, max_tokens: int = 4096, role: str = "llm") -> str:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        candidates = [m for m in (model, config.FALLBACK_MODEL) if m not in self._dead_models]
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
