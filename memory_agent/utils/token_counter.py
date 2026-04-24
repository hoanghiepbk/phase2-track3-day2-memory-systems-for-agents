"""
Token counter — uses tiktoken for accurate OpenAI token counting.

Falls back to word-count estimation if tiktoken is unavailable.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    import tiktoken

    _ENCODER = tiktoken.encoding_for_model("gpt-4o-mini")
    _TIKTOKEN_AVAILABLE = True
except Exception:
    _TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available — falling back to word-count estimation.")


def count_tokens(text: str) -> int:
    """Return the number of tokens in *text*."""
    if _TIKTOKEN_AVAILABLE:
        return len(_ENCODER.encode(text))
    # Rough approximation: 1 token ≈ 0.75 words
    return int(len(text.split()) / 0.75)


def trim_to_budget(text: str, budget: int) -> str:
    """Trim *text* from the front so that it fits within *budget* tokens."""
    if count_tokens(text) <= budget:
        return text

    if _TIKTOKEN_AVAILABLE:
        tokens = _ENCODER.encode(text)
        trimmed_tokens = tokens[-budget:]
        return _ENCODER.decode(trimmed_tokens)

    # Word-level fallback
    words = text.split()
    target_words = int(budget * 0.75)
    return " ".join(words[-target_words:])


def estimate_messages_tokens(messages: list[dict[str, str]]) -> int:
    """Estimate total tokens across a list of chat messages."""
    total = 0
    for msg in messages:
        # ~4 tokens overhead per message (role, delimiters)
        total += 4
        total += count_tokens(msg.get("content", ""))
    return total
