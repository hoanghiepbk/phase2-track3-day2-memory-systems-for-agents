"""
LangGraph node functions — each node reads/writes MemoryState.

Node pipeline:
    retrieve_memory → build_prompt → call_llm → save_memory
"""

from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

from memory_agent.config import OPENAI_API_KEY, OPENAI_MODEL, MEMORY_TOKEN_BUDGET
from memory_agent.graph.state import MemoryState
from memory_agent.graph.router import MemoryRouter
from memory_agent.prompts.templates import build_system_prompt, NO_MEMORY_SYSTEM_PROMPT
from memory_agent.utils.extractor import extract_facts
from memory_agent.utils.token_counter import count_tokens

logger = logging.getLogger(__name__)

# Module-level OpenAI client (reused across calls)
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


# ======================================================================
# Node: retrieve_memory
# ======================================================================
def make_retrieve_memory_node(router: MemoryRouter):
    """Factory that creates a retrieve_memory node bound to a specific router."""

    def retrieve_memory(state: dict[str, Any]) -> dict[str, Any]:
        """Retrieve relevant context from all four memory backends."""
        user_id = state.get("user_id", "default")
        query = state.get("current_query", "")

        if not query and state.get("messages"):
            # Fallback: use last user message
            for msg in reversed(state["messages"]):
                if msg.get("role") == "user":
                    query = msg["content"]
                    break

        memory_data = router.retrieve_all(
            user_id=user_id,
            query=query,
            token_budget=state.get("memory_budget", MEMORY_TOKEN_BUDGET),
        )

        return {
            "user_profile": memory_data["user_profile"],
            "episodes": memory_data["episodes"],
            "semantic_hits": memory_data["semantic_hits"],
            "memory_budget": memory_data["memory_budget"],
        }

    return retrieve_memory


# ======================================================================
# Node: call_llm (with memory)
# ======================================================================
def call_llm(state: dict[str, Any]) -> dict[str, Any]:
    """Build prompt with injected memory and call the LLM."""
    # Build system prompt with all 4 memory sections
    system_prompt = build_system_prompt(
        profile=state.get("user_profile", {}),
        episodes=state.get("episodes", []),
        semantic_hits=state.get("semantic_hits", []),
    )

    # Prepare messages: system + conversation history
    api_messages = [{"role": "system", "content": system_prompt}]

    # Add conversation messages (short-term memory is here)
    for msg in state.get("messages", []):
        api_messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
        })

    logger.info(
        "Calling LLM with %d messages, system prompt: %d tokens.",
        len(api_messages),
        count_tokens(system_prompt),
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=api_messages,
        temperature=0.7,
        max_tokens=1000,
    )

    assistant_msg = response.choices[0].message.content or ""
    usage = response.usage

    token_usage = {
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }

    return {
        "response": assistant_msg,
        "token_usage": token_usage,
    }


# ======================================================================
# Node: call_llm_no_memory (baseline for benchmark)
# ======================================================================
def call_llm_no_memory(state: dict[str, Any]) -> dict[str, Any]:
    """Call the LLM without any memory context (benchmark baseline)."""
    api_messages = [{"role": "system", "content": NO_MEMORY_SYSTEM_PROMPT}]

    for msg in state.get("messages", []):
        api_messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
        })

    client = _get_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=api_messages,
        temperature=0.7,
        max_tokens=1000,
    )

    assistant_msg = response.choices[0].message.content or ""
    usage = response.usage

    return {
        "response": assistant_msg,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        },
    }


# ======================================================================
# Node: save_memory
# ======================================================================
def make_save_memory_node(router: MemoryRouter):
    """Factory that creates a save_memory node bound to a specific router."""

    def save_memory(state: dict[str, Any]) -> dict[str, Any]:
        """
        Post-response: extract facts and save to appropriate backends.

        - Short-term: append assistant response to buffer
        - Long-term: extract & upsert user profile facts
        - Episodic: save completed task episodes
        """
        user_id = state.get("user_id", "default")
        response = state.get("response", "")
        messages = state.get("messages", [])

        # 1. Save assistant response to short-term memory
        if response:
            router.short_term.store("msg", {"role": "assistant", "content": response})

        # 2. Extract and update user profile facts (LLM-based)
        user_messages = [m for m in messages if m.get("role") == "user"]
        if user_messages:
            try:
                new_facts = extract_facts(messages)
                if new_facts:
                    router.long_term.store(user_id, new_facts)
                    logger.info("Updated profile for user '%s': %s", user_id, list(new_facts.keys()))
            except Exception as exc:
                logger.error("Fact extraction failed: %s", exc)

        # 3. Check if this looks like a completed task → save episode
        query = state.get("current_query", "")
        if _is_task_completion(query, response):
            episode = {
                "task": query,
                "trajectory": f"User asked: {query}",
                "outcome": response[:200],  # Truncate for storage
                "reflection": f"Successfully answered question about: {query[:100]}",
            }
            router.episodic.store(user_id, episode)

        return state

    return save_memory


def _is_task_completion(query: str, response: str) -> bool:
    """Heuristic: save episode when the interaction looks like a completed task."""
    if not query or not response:
        return False
    # Save episodes for substantive exchanges (not just greetings)
    task_indicators = [
        "how", "what", "why", "explain", "help", "fix", "debug",
        "làm sao", "tại sao", "giải thích", "hướng dẫn", "giúp",
        "cách", "lỗi", "sửa",
    ]
    query_lower = query.lower()
    return any(indicator in query_lower for indicator in task_indicators) and len(response) > 50
