"""
main.py — Interactive Multi-Memory Agent with LangGraph.
Run:  python main.py
"""
from __future__ import annotations
import logging, sys
from memory_agent.config import OPENAI_API_KEY, MEMORY_TOKEN_BUDGET
from memory_agent.graph.builder import build_memory_agent_graph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")

def main() -> None:
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)
    print("=" * 60)
    print("  Multi-Memory Agent (LangGraph)")
    print("=" * 60)
    print("Commands:  /quit  /clear  /profile  /episodes")
    print("=" * 60)
    graph, router = build_memory_agent_graph(ingest_knowledge=True)
    user_id = "user_001"
    messages: list[dict[str, str]] = []
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() == "/quit":
            print("Goodbye!")
            break
        if user_input.lower() == "/clear":
            router.short_term.clear()
            messages.clear()
            print("Short-term memory cleared.")
            continue
        if user_input.lower() == "/profile":
            profile = router.long_term.retrieve(user_id)
            if profile:
                print("\nUser Profile:")
                for k, v in profile.items():
                    print(f"  {k}: {v}")
            else:
                print("No profile data yet.")
            continue
        if user_input.lower() == "/episodes":
            eps = router.episodic.retrieve_by_user(user_id, k=5)
            if eps:
                print(f"\nRecent Episodes ({len(eps)}):")
                for i, ep in enumerate(eps, 1):
                    print(f"  {i}. {ep['task'][:80]}")
                    print(f"     Outcome: {ep['outcome'][:80]}")
            else:
                print("No episodes recorded yet.")
            continue
        user_msg = {"role": "user", "content": user_input}
        router.short_term.store("msg", user_msg)
        messages.append(user_msg)
        state = {
            "messages": list(messages),
            "current_query": user_input,
            "user_id": user_id,
            "user_profile": {},
            "episodes": [],
            "semantic_hits": [],
            "memory_budget": MEMORY_TOKEN_BUDGET,
            "response": "",
            "token_usage": {},
        }
        try:
            result = graph.invoke(state)
        except Exception as exc:
            logger.error("Graph invocation failed: %s", exc)
            print(f"Error: {exc}")
            continue
        response = result.get("response", "")
        token_usage = result.get("token_usage", {})
        assistant_msg = {"role": "assistant", "content": response}
        messages.append(assistant_msg)
        print(f"\nAgent: {response}")
        if token_usage:
            print(f"  Tokens: {token_usage.get('prompt_tokens',0)} prompt + {token_usage.get('completion_tokens',0)} completion = {token_usage.get('total_tokens',0)} total")

if __name__ == "__main__":
    main()
