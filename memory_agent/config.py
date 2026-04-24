"""
Configuration module — loads settings from .env with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# ---------------------------------------------------------------------------
# Memory Tuning
# ---------------------------------------------------------------------------
SHORT_TERM_MAX_MESSAGES: int = int(os.getenv("SHORT_TERM_MAX_MESSAGES", "20"))
MEMORY_TOKEN_BUDGET: int = int(os.getenv("MEMORY_TOKEN_BUDGET", "3000"))
EPISODIC_MAX_EPISODES: int = int(os.getenv("EPISODIC_MAX_EPISODES", "50"))
SEMANTIC_TOP_K: int = int(os.getenv("SEMANTIC_TOP_K", "3"))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
PROFILES_DIR = DATA_DIR / "profiles"
EPISODES_DIR = DATA_DIR / "episodes"
KNOWLEDGE_DIR = DATA_DIR / "knowledge_base"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# Ensure directories exist
for d in [PROFILES_DIR, EPISODES_DIR, KNOWLEDGE_DIR, CHROMA_DIR]:
    d.mkdir(parents=True, exist_ok=True)
