"""
Short-Term Memory — Sliding-window conversation buffer.

Keeps the most recent *max_messages* turns (user + assistant pairs).
When the window is exceeded the oldest messages are evicted.
"""

from __future__ import annotations

import logging
from typing import Any

from memory_agent.memory.base import MemoryInterface

logger = logging.getLogger(__name__)


class ShortTermMemory(MemoryInterface):
    """In-process sliding-window buffer over conversation messages."""

    def __init__(self, max_messages: int = 20) -> None:
        self._buffer: list[dict[str, str]] = []
        self._max_messages = max_messages

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def store(self, key: str, data: Any) -> None:
        """Append a message ``{"role": ..., "content": ...}`` to the buffer."""
        if not isinstance(data, dict) or "role" not in data or "content" not in data:
            raise ValueError("ShortTermMemory expects {'role': str, 'content': str}")
        self._buffer.append(data)
        self._trim()

    def retrieve(self, query: str = "", k: int = 0) -> list[dict[str, str]]:
        """Return the full buffer (most-recent *max_messages* turns)."""
        return list(self._buffer)

    def clear(self) -> None:
        self._buffer.clear()
        logger.info("Short-term memory cleared.")

    def delete(self, key: str) -> bool:
        """Remove messages whose content contains *key*."""
        before = len(self._buffer)
        self._buffer = [m for m in self._buffer if key not in m.get("content", "")]
        removed = before - len(self._buffer)
        if removed:
            logger.info("Removed %d message(s) matching '%s'.", removed, key)
        return removed > 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _trim(self) -> None:
        """Evict oldest messages when buffer exceeds the sliding window."""
        if len(self._buffer) > self._max_messages:
            overflow = len(self._buffer) - self._max_messages
            self._buffer = self._buffer[overflow:]
            logger.debug("Trimmed %d oldest message(s) from short-term memory.", overflow)

    def __len__(self) -> int:
        return len(self._buffer)

    def __repr__(self) -> str:
        return f"ShortTermMemory(messages={len(self._buffer)}, max={self._max_messages})"
