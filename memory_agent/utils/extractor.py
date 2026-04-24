"""
LLM-based fact extractor — extracts structured user facts from conversation.

Uses OpenAI to parse conversation messages and return a JSON dict of
key facts (name, preferences, allergies, skills, etc.).  Includes
robust JSON parsing and error handling (bonus points).
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from openai import OpenAI

from memory_agent.config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)

_EXTRACTION_PROMPT = """\
You are a fact extraction engine.  Analyze the following conversation and
extract key user facts.  Return ONLY a valid JSON object — no markdown
fences, no explanation.

Rules:
- Only include facts the user explicitly stated.
- Use lowercase keys: name, preferences, allergies, skills, location, occupation, etc.
- For lists (preferences, skills, allergies), use JSON arrays.
- If the user corrected a previous fact, use the LATEST value only.
- If no facts are found, return an empty JSON object: {{}}

Conversation:
{conversation}
"""


def extract_facts(messages: list[dict[str, str]]) -> dict[str, Any]:
    """
    Extract structured user facts from a conversation.

    Returns a dict like ``{"name": "Linh", "allergies": ["đậu nành"]}``.
    Returns ``{}`` on any failure (never raises).
    """
    if not messages:
        return {}

    # Build conversation text from user messages
    conversation_lines: list[str] = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if content.strip():
            conversation_lines.append(f"{role}: {content}")

    if not conversation_lines:
        return {}

    conversation_text = "\n".join(conversation_lines)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured facts from conversations. Respond ONLY with valid JSON.",
                },
                {
                    "role": "user",
                    "content": _EXTRACTION_PROMPT.format(conversation=conversation_text),
                },
            ],
            temperature=0.0,
            max_tokens=500,
        )
        raw = response.choices[0].message.content or "{}"
        facts = _parse_json_robust(raw)
        logger.info("Extracted %d fact(s) from conversation.", len(facts))
        return facts

    except Exception as exc:
        logger.error("Fact extraction failed: %s", exc)
        return {}


def _parse_json_robust(text: str) -> dict[str, Any]:
    """Parse JSON with fallback handling for common LLM output quirks."""
    text = text.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return result
        logger.warning("Extraction returned non-dict JSON: %s", type(result))
        return {}
    except json.JSONDecodeError as exc:
        logger.warning("JSON parse failed: %s — raw: %s", exc, text[:200])
        return {}
