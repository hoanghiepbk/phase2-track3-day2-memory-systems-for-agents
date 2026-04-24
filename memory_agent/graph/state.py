"""
LangGraph state definition — the single source of truth flowing through the graph.
"""

from __future__ import annotations

from typing import Any, TypedDict


class MemoryState(TypedDict, total=False):
    """
    State object passed between LangGraph nodes.

    Attributes
    ----------
    messages : list[dict]
        Full conversation history (role + content dicts).
    current_query : str
        The latest user message being processed.
    user_id : str
        Identifier for the current user.
    user_profile : dict
        Long-term profile facts retrieved from the profile store.
    episodes : list[dict]
        Relevant past episodes retrieved from episodic memory.
    semantic_hits : list[str]
        Document chunks retrieved from semantic/vector memory.
    memory_budget : int
        Remaining token budget after memory injection.
    response : str
        The assistant's generated response.
    token_usage : dict[str, int]
        Token counts: prompt_tokens, completion_tokens, total_tokens.
    """

    messages: list[dict[str, str]]
    current_query: str
    user_id: str
    user_profile: dict[str, Any]
    episodes: list[dict[str, Any]]
    semantic_hits: list[str]
    memory_budget: int
    response: str
    token_usage: dict[str, int]
