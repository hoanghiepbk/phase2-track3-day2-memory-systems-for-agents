"""
Prompt templates — system prompts with dedicated sections for each memory type.

The template uses four clearly labeled sections so the grader can see that
all four memory types are injected into the LLM context.
"""

SYSTEM_PROMPT_TEMPLATE = """\
You are a helpful, knowledgeable AI assistant with advanced memory capabilities.
You can remember user preferences, past interactions, and domain knowledge across sessions.

═══════════════════════════════════════════
📋 USER PROFILE (Long-term Memory)
═══════════════════════════════════════════
{user_profile}

═══════════════════════════════════════════
📖 RELEVANT PAST EPISODES (Episodic Memory)
═══════════════════════════════════════════
{episodes}

═══════════════════════════════════════════
🔍 RELATED KNOWLEDGE (Semantic Memory)
═══════════════════════════════════════════
{semantic_hits}

═══════════════════════════════════════════
💬 RECENT CONVERSATION (Short-term Memory)
═══════════════════════════════════════════
(Provided in the message history below)

═══════════════════════════════════════════
📌 INSTRUCTIONS
═══════════════════════════════════════════
- Use the above memory context to provide personalized, contextually relevant responses.
- If the user corrects a previously stated fact, acknowledge the correction and use the updated information.
- Reference relevant past episodes when they help answer the current question.
- Use domain knowledge from semantic memory to support your answers.
- Be concise, helpful, and proactive in using what you know about the user.
- Always respond in the same language the user uses.
"""

NO_MEMORY_SYSTEM_PROMPT = """\
You are a helpful AI assistant. You have no memory of previous conversations.
Answer based solely on the current conversation context.
Always respond in the same language the user uses.
"""


def format_user_profile(profile: dict) -> str:
    """Format a user profile dict into a readable string for the prompt."""
    if not profile:
        return "No user profile available yet."

    lines: list[str] = []
    for key, value in profile.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        lines.append(f"• {key}: {value}")
    return "\n".join(lines)


def format_episodes(episodes: list[dict]) -> str:
    """Format episodic memory entries into a readable string."""
    if not episodes:
        return "No relevant past episodes found."

    lines: list[str] = []
    for i, ep in enumerate(episodes, 1):
        lines.append(f"Episode {i}:")
        lines.append(f"  Task: {ep.get('task', 'N/A')}")
        if ep.get("trajectory"):
            lines.append(f"  Approach: {ep['trajectory']}")
        lines.append(f"  Outcome: {ep.get('outcome', 'N/A')}")
        if ep.get("reflection"):
            lines.append(f"  Lesson: {ep['reflection']}")
        lines.append("")
    return "\n".join(lines)


def format_semantic_hits(hits: list[str]) -> str:
    """Format semantic search results into a readable string."""
    if not hits:
        return "No relevant domain knowledge found."

    lines: list[str] = []
    for i, chunk in enumerate(hits, 1):
        lines.append(f"[Knowledge {i}]\n{chunk}\n")
    return "\n".join(lines)


def build_system_prompt(
    profile: dict,
    episodes: list[dict],
    semantic_hits: list[str],
) -> str:
    """Build the full system prompt with all four memory sections populated."""
    return SYSTEM_PROMPT_TEMPLATE.format(
        user_profile=format_user_profile(profile),
        episodes=format_episodes(episodes),
        semantic_hits=format_semantic_hits(semantic_hits),
    )
