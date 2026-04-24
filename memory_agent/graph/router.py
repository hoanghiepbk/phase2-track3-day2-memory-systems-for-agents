"""
Memory router — selects and retrieves from appropriate memory backends
based on the current query context.
"""

from __future__ import annotations

import logging
from typing import Any

from memory_agent.memory import (
    ShortTermMemory,
    LongTermProfileMemory,
    EpisodicMemory,
    SemanticMemory,
)
from memory_agent.utils.token_counter import count_tokens

logger = logging.getLogger(__name__)


class MemoryRouter:
    """
    Routes queries to the appropriate memory backends and merges results.

    Priority order (from slide):
        1. Short-term  (recent conversation — already in messages)
        2. Long-term   (user profile/preferences)
        3. Episodic    (past task experiences)
        4. Semantic    (domain knowledge chunks)
    """

    def __init__(
        self,
        short_term: ShortTermMemory,
        long_term: LongTermProfileMemory,
        episodic: EpisodicMemory,
        semantic: SemanticMemory,
    ) -> None:
        self.short_term = short_term
        self.long_term = long_term
        self.episodic = episodic
        self.semantic = semantic

    def retrieve_all(
        self,
        user_id: str,
        query: str,
        token_budget: int = 3000,
    ) -> dict[str, Any]:
        """
        Retrieve from all four memory backends with token budget management.

        Returns a dict with keys: user_profile, episodes, semantic_hits,
        memory_budget (remaining tokens).
        """
        remaining = token_budget

        # Priority 1: Short-term is already in state.messages — no retrieval needed
        # (it's the sliding-window conversation buffer)

        # Priority 2: Long-term profile
        user_profile = self.long_term.retrieve(user_id)
        profile_tokens = count_tokens(str(user_profile)) if user_profile else 0
        remaining -= profile_tokens

        # Priority 3: Episodic recall
        episodes: list[dict[str, Any]] = []
        if remaining > 200:
            raw_episodes = self.episodic.retrieve(query, k=3)
            for ep in raw_episodes:
                ep_tokens = count_tokens(str(ep))
                if remaining - ep_tokens < 100:
                    break
                episodes.append(ep)
                remaining -= ep_tokens

        # Priority 4: Semantic search
        semantic_hits: list[str] = []
        if remaining > 200:
            raw_hits = self.semantic.retrieve(query, k=3)
            for hit in raw_hits:
                hit_tokens = count_tokens(hit)
                if remaining - hit_tokens < 100:
                    break
                semantic_hits.append(hit)
                remaining -= hit_tokens

        logger.info(
            "Memory retrieval complete — profile: %d tokens, "
            "episodes: %d (%d items), semantic: %d (%d items), "
            "remaining budget: %d tokens.",
            profile_tokens,
            sum(count_tokens(str(e)) for e in episodes),
            len(episodes),
            sum(count_tokens(h) for h in semantic_hits),
            len(semantic_hits),
            remaining,
        )

        return {
            "user_profile": user_profile,
            "episodes": episodes,
            "semantic_hits": semantic_hits,
            "memory_budget": remaining,
        }
