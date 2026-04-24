"""
Episodic Memory — JSON-based log of past task episodes.

Each episode stores: (task, trajectory, outcome, reflection, timestamp).
Retrieval uses keyword similarity to find episodes relevant to the
current query.  Episodes are persisted as JSONL files per user.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from memory_agent.memory.base import MemoryInterface

logger = logging.getLogger(__name__)


class EpisodicMemory(MemoryInterface):
    """JSONL-backed store of task episodes with keyword-based retrieval."""

    def __init__(self, persist_dir: Path | str, max_episodes: int = 50) -> None:
        self._persist_dir = Path(persist_dir)
        self._persist_dir.mkdir(parents=True, exist_ok=True)
        self._max_episodes = max_episodes
        self._episodes: dict[str, list[dict[str, Any]]] = {}
        self._load_all()

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def store(self, key: str, data: Any) -> None:
        """
        Append an episode for user *key*.

        *data* must be a dict with at least ``task`` and ``outcome``:

        .. code-block:: python

            {
                "task": "Debug Docker networking issue",
                "trajectory": "Tried bridge network, then host network",
                "outcome": "Host network solved the issue",
                "reflection": "Docker bridge network doesn't expose ports by default",
            }
        """
        if not isinstance(data, dict) or "task" not in data:
            raise ValueError("EpisodicMemory expects a dict with at least a 'task' key.")

        episode = {
            "task": data.get("task", ""),
            "trajectory": data.get("trajectory", ""),
            "outcome": data.get("outcome", ""),
            "reflection": data.get("reflection", ""),
            "timestamp": datetime.now().isoformat(),
        }

        if key not in self._episodes:
            self._episodes[key] = []
        self._episodes[key].append(episode)

        # LRU eviction: drop oldest episodes when exceeding max
        if len(self._episodes[key]) > self._max_episodes:
            evicted = len(self._episodes[key]) - self._max_episodes
            self._episodes[key] = self._episodes[key][evicted:]
            logger.debug("Evicted %d oldest episode(s) for user '%s'.", evicted, key)

        self._persist(key)
        logger.info("Stored episode for user '%s': %s", key, episode["task"])

    def retrieve(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        """
        Return up to *k* episodes most relevant to *query*.

        Relevance is scored by keyword overlap between the query and the
        episode's task + outcome + reflection text.
        """
        all_episodes: list[dict[str, Any]] = []
        for episodes in self._episodes.values():
            all_episodes.extend(episodes)

        if not all_episodes:
            return []

        query_tokens = set(query.lower().split())

        def _score(ep: dict[str, Any]) -> float:
            text = f"{ep['task']} {ep['outcome']} {ep['reflection']}".lower()
            ep_tokens = set(text.split())
            overlap = query_tokens & ep_tokens
            return len(overlap) / max(len(query_tokens), 1)

        scored = sorted(all_episodes, key=_score, reverse=True)
        return scored[:k]

    def retrieve_by_user(self, user_id: str, k: int = 5) -> list[dict[str, Any]]:
        """Return the *k* most recent episodes for a specific user."""
        episodes = self._episodes.get(user_id, [])
        return episodes[-k:]

    def clear(self) -> None:
        self._episodes.clear()
        for fp in self._persist_dir.glob("*.jsonl"):
            fp.unlink()
        logger.info("Episodic memory cleared.")

    def delete(self, key: str) -> bool:
        if key in self._episodes:
            del self._episodes[key]
            fp = self._persist_dir / f"{key}.jsonl"
            if fp.exists():
                fp.unlink()
            logger.info("Deleted episodes for user '%s'.", key)
            return True
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _persist(self, user_id: str) -> None:
        fp = self._persist_dir / f"{user_id}.jsonl"
        with open(fp, "w", encoding="utf-8") as f:
            for ep in self._episodes.get(user_id, []):
                f.write(json.dumps(ep, ensure_ascii=False) + "\n")

    def _load_all(self) -> None:
        for fp in self._persist_dir.glob("*.jsonl"):
            user_id = fp.stem
            episodes: list[dict[str, Any]] = []
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        episodes.append(json.loads(line))
            self._episodes[user_id] = episodes
        total = sum(len(v) for v in self._episodes.values())
        if total:
            logger.info("Loaded %d episode(s) from disk.", total)

    def __repr__(self) -> str:
        total = sum(len(v) for v in self._episodes.values())
        return f"EpisodicMemory(episodes={total}, max={self._max_episodes})"
