"""
LangGraph graph builder — assembles nodes into a compiled graph.

Graph flow:
    START → retrieve_memory → call_llm → save_memory → END
"""

from __future__ import annotations

import logging

from langgraph.graph import START, END, StateGraph

from memory_agent.config import (
    SHORT_TERM_MAX_MESSAGES,
    MEMORY_TOKEN_BUDGET,
    EPISODIC_MAX_EPISODES,
    SEMANTIC_TOP_K,
    PROFILES_DIR,
    EPISODES_DIR,
    CHROMA_DIR,
    KNOWLEDGE_DIR,
)
from memory_agent.graph.nodes import (
    make_retrieve_memory_node,
    call_llm,
    call_llm_no_memory,
    make_save_memory_node,
)
from memory_agent.graph.router import MemoryRouter
from memory_agent.graph.state import MemoryState
from memory_agent.memory import (
    ShortTermMemory,
    LongTermProfileMemory,
    EpisodicMemory,
    SemanticMemory,
)

logger = logging.getLogger(__name__)


def _init_memory_backends() -> tuple[
    ShortTermMemory, LongTermProfileMemory, EpisodicMemory, SemanticMemory
]:
    """Instantiate all four memory backends."""
    short_term = ShortTermMemory(max_messages=SHORT_TERM_MAX_MESSAGES)
    long_term = LongTermProfileMemory(persist_dir=PROFILES_DIR)
    episodic = EpisodicMemory(persist_dir=EPISODES_DIR, max_episodes=EPISODIC_MAX_EPISODES)
    semantic = SemanticMemory(persist_dir=CHROMA_DIR)
    return short_term, long_term, episodic, semantic


def build_memory_agent_graph(
    ingest_knowledge: bool = True,
) -> tuple[StateGraph, MemoryRouter]:
    """
    Build and return the compiled LangGraph for the memory-enabled agent.

    Returns
    -------
    graph : CompiledGraph
        The compiled LangGraph ready for invocation.
    router : MemoryRouter
        The router instance (useful for direct backend access in tests).
    """
    # 1. Initialise backends
    short_term, long_term, episodic, semantic = _init_memory_backends()

    # 2. Ingest domain knowledge into semantic memory
    if ingest_knowledge:
        ingested = semantic.ingest_directory(KNOWLEDGE_DIR)
        logger.info("Ingested %d knowledge chunks into semantic memory.", ingested)

    # 3. Create router
    router = MemoryRouter(
        short_term=short_term,
        long_term=long_term,
        episodic=episodic,
        semantic=semantic,
    )

    # 4. Create node functions bound to this router
    retrieve_memory = make_retrieve_memory_node(router)
    save_memory = make_save_memory_node(router)

    # 5. Build LangGraph
    graph_builder = StateGraph(MemoryState)

    # Add nodes
    graph_builder.add_node("retrieve_memory", retrieve_memory)
    graph_builder.add_node("call_llm", call_llm)
    graph_builder.add_node("save_memory", save_memory)

    # Define edges: START → retrieve → llm → save → END
    graph_builder.add_edge(START, "retrieve_memory")
    graph_builder.add_edge("retrieve_memory", "call_llm")
    graph_builder.add_edge("call_llm", "save_memory")
    graph_builder.add_edge("save_memory", END)

    compiled = graph_builder.compile()
    logger.info("Memory agent graph compiled successfully.")

    return compiled, router


def build_no_memory_agent_graph() -> StateGraph:
    """
    Build a baseline agent graph WITHOUT memory (for benchmark comparison).

    Graph: START → call_llm_no_memory → END
    """
    graph_builder = StateGraph(MemoryState)
    graph_builder.add_node("call_llm", call_llm_no_memory)
    graph_builder.add_edge(START, "call_llm")
    graph_builder.add_edge("call_llm", END)

    compiled = graph_builder.compile()
    logger.info("No-memory baseline graph compiled successfully.")
    return compiled
