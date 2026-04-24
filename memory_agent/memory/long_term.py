"""
Long-Term Profile Memory — Persistent user profile store.

Uses a dict-based in-memory store backed by JSON files on disk.
Provides a Redis-like interface (hgetall / hset) so the architecture
mirrors a production Redis deployment while staying dependency-free.

Conflict resolution: **recency wins** — when a fact key already exists,
the new value replaces the old one and the change is logged.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from memory_agent.memory.base import MemoryInterface

logger = logging.getLogger(__name__)


class LongTermProfileMemory(MemoryInterface):
    """Dict + JSON-file backed user-profile store."""

    def __init__(self, persist_dir: Path | str) -> None:
        self._persist_dir = Path(persist_dir)
        self._persist_dir.mkdir(parents=True, exist_ok=True)
        self._profiles: dict[str, dict[str, Any]] = {}
        self._load_all()

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def store(self, key: str, data: Any) -> None:
        """
        Upsert user profile.

        *key*  — user_id
        *data* — dict of facts, e.g. ``{"name": "Linh", "allergy": "đậu nành"}``
        """
        if not isinstance(data, dict):
            raise ValueError("LongTermProfileMemory expects a dict of profile facts.")

        existing = self._profiles.get(key, {})
        conflicts: list[str] = []

        for fact_key, fact_value in data.items():
            if fact_key in existing and existing[fact_key] != fact_value:
                conflicts.append(
                    f"  {fact_key}: '{existing[fact_key]}' → '{fact_value}'"
                )
            existing[fact_key] = fact_value

        existing["_last_updated"] = datetime.now().isoformat()
        self._profiles[key] = existing

        if conflicts:
            logger.info(
                "Conflict resolution (recency wins) for user '%s':\n%s",
                key,
                "\n".join(conflicts),
            )

        self._persist(key)

    def retrieve(self, query: str, k: int = 0) -> dict[str, Any]:
        """Return the full profile dict for user *query* (user_id)."""
        profile = self._profiles.get(query, {})
        # Filter internal keys for external consumers
        return {k: v for k, v in profile.items() if not k.startswith("_")}

    def clear(self) -> None:
        self._profiles.clear()
        # Remove all JSON files
        for fp in self._persist_dir.glob("*.json"):
            fp.unlink()
        logger.info("Long-term profile memory cleared.")

    def delete(self, key: str) -> bool:
        """Delete a user's entire profile (GDPR right-to-be-forgotten)."""
        if key in self._profiles:
            del self._profiles[key]
            fp = self._persist_dir / f"{key}.json"
            if fp.exists():
                fp.unlink()
            logger.info("Deleted profile for user '%s'.", key)
            return True
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _persist(self, user_id: str) -> None:
        fp = self._persist_dir / f"{user_id}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(self._profiles[user_id], f, ensure_ascii=False, indent=2)

    def _load_all(self) -> None:
        for fp in self._persist_dir.glob("*.json"):
            user_id = fp.stem
            with open(fp, "r", encoding="utf-8") as f:
                self._profiles[user_id] = json.load(f)
        if self._profiles:
            logger.info("Loaded %d profile(s) from disk.", len(self._profiles))

    def __repr__(self) -> str:
        return f"LongTermProfileMemory(users={len(self._profiles)})"
