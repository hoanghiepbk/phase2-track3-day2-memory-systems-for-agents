"""
Abstract base class for all memory backends.

Every memory type (short-term, long-term, episodic, semantic) implements
this interface so the router can interact with them uniformly while each
backend maintains its own storage/retrieval logic.
"""

from abc import ABC, abstractmethod
from typing import Any


class MemoryInterface(ABC):
    """Unified interface for all memory backends."""

    @abstractmethod
    def store(self, key: str, data: Any) -> None:
        """Persist data under *key*."""

    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> Any:
        """Return up to *k* relevant items matching *query*."""

    @abstractmethod
    def clear(self) -> None:
        """Wipe all entries from this backend."""

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a specific entry.  Returns True if something was removed."""
