"""Central configuration. Everything tunable lives here or in .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# ---- Models (Groq) ----------------------------------------------------------
# Generator and evaluator use DIFFERENT models on purpose, so the system is not
# grading its own homework with the same blind spots.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GENERATOR_MODEL = os.getenv("GENERATOR_MODEL", "llama-3.3-70b-versatile")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "openai/gpt-oss-120b")
# Used automatically if a configured model is unavailable on the account.
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "llama-3.1-8b-instant")

GENERATOR_TEMPERATURE = float(os.getenv("GENERATOR_TEMPERATURE", "0.6"))
EVALUATOR_TEMPERATURE = 0.0  # judges must be as deterministic as possible

# ---- Loop control -----------------------------------------------------------
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))  # => at most 1 + 2 = 3 attempts

# ---- Self-evolving memory ---------------------------------------------------
MEMORY_DB = Path(os.getenv("MEMORY_DB", ROOT / "memory" / "memory.db"))
# A check must fail this many times (across runs) before the system distils a
# permanent "lesson learned" rule for the generator.
RULE_PROMOTION_THRESHOLD = int(os.getenv("RULE_PROMOTION_THRESHOLD", "2"))
MAX_ACTIVE_RULES = 12          # cap so the prompt does not grow forever
MAX_JUDGE_EXAMPLES_PER_CHECK = 3  # past failure examples shown to the judge

# ---- Paths ------------------------------------------------------------------
SOURCES_DIR = ROOT / "sources"
OUTPUTS_DIR = ROOT / "outputs"

# ---- Deterministic rubric thresholds ---------------------------------------
MIN_WORDS = 900
MAX_WORDS = 2300
MIN_FLESCH_READING_EASE = 60.0   # 60-70 = "plain English", easily understood by ~15 year olds
MAX_AVG_SENTENCE_WORDS = 17.0
MAX_SENTENCE_WORDS = 32
MIN_QUIZ_QUESTIONS = 3
MIN_EXAMPLES = 2
