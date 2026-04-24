# Lab #17: Multi-Memory Agent with LangGraph

Build a production-grade AI agent with a **4-type memory stack** using LangGraph,
with benchmark comparison of agent performance with and without memory.

## Architecture

```
                    ┌─────────────────┐
                    │   User Input    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ retrieve_memory │ ← Memory Router
                    │  (LangGraph)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                     │
   ┌────▼─────┐      ┌──────▼──────┐      ┌──────▼──────┐
   │Long-term │      │  Episodic   │      │  Semantic   │
   │ Profile  │      │   Memory    │      │   Memory    │
   │(JSON/KV) │      │  (JSONL)    │      │ (ChromaDB)  │
   └──────────┘      └─────────────┘      └─────────────┘
                             │
                    ┌────────▼────────┐
                    │   call_llm      │ ← Prompt with 4 memory sections
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  save_memory    │ ← Extract facts + save episodes
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Response     │
                    └─────────────────┘
```

## Memory Types

| Type | Backend | Purpose |
|------|---------|---------|
| **Short-term** | Sliding window buffer | Current conversation context |
| **Long-term Profile** | Dict + JSON persistence | User preferences, facts across sessions |
| **Episodic** | JSONL log files | Past task outcomes and lessons learned |
| **Semantic** | ChromaDB (vector search) | Domain knowledge retrieval |

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run interactive agent
```bash
python main.py
```

### 4. Run benchmark (10 multi-turn conversations)
```bash
python -m benchmark.run_benchmark
```

## Project Structure

```
├── memory_agent/
│   ├── config.py              # Settings from .env
│   ├── memory/
│   │   ├── base.py            # Abstract MemoryInterface
│   │   ├── short_term.py      # Sliding window buffer
│   │   ├── long_term.py       # Profile store (conflict handling)
│   │   ├── episodic.py        # Task episode logs
│   │   └── semantic.py        # ChromaDB vector search
│   ├── graph/
│   │   ├── state.py           # MemoryState TypedDict
│   │   ├── nodes.py           # LangGraph node functions
│   │   ├── router.py          # Memory router (priority-based)
│   │   └── builder.py         # Graph assembly
│   ├── prompts/
│   │   └── templates.py       # System prompt with 4 memory sections
│   └── utils/
│       ├── token_counter.py   # tiktoken-based counting
│       └── extractor.py       # LLM fact extraction
├── data/knowledge_base/       # Domain docs for semantic memory
├── benchmark/
│   └── run_benchmark.py       # 10-scenario benchmark runner
├── main.py                    # Interactive CLI
├── BENCHMARK.md               # Generated benchmark report
└── requirements.txt
```

## Key Features

- **4 memory types** with separate interfaces and backends
- **LangGraph** state/router with clear node pipeline
- **Conflict resolution**: recency-wins with logging
- **Token budget management**: tiktoken-based with priority eviction
- **LLM fact extraction**: Structured JSON output with error handling
- **GDPR support**: delete methods on all backends
- **Benchmark**: 10 multi-turn conversations across 5 test groups
