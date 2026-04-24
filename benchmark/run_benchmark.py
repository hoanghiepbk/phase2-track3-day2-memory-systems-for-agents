"""
Benchmark runner — runs 10 multi-turn conversations comparing
no-memory vs with-memory agent, then generates BENCHMARK.md.

Run:  python -m benchmark.run_benchmark
"""
from __future__ import annotations
import json, logging, sys, time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from memory_agent.config import OPENAI_API_KEY, MEMORY_TOKEN_BUDGET
from memory_agent.graph.builder import build_memory_agent_graph, build_no_memory_agent_graph
from memory_agent.utils.token_counter import count_tokens

logging.basicConfig(level=logging.WARNING, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("benchmark")
logger.setLevel(logging.INFO)

# ── 10 multi-turn conversation scenarios ─────────────────────────────
SCENARIOS = [
    {
        "id": 1,
        "name": "Recall user name after 6 turns",
        "group": "profile_recall",
        "setup_turns": [
            {"role": "user", "content": "Xin chào, tôi tên là Linh."},
            {"role": "user", "content": "Hôm nay thời tiết đẹp quá nhỉ?"},
            {"role": "user", "content": "Bạn có thể giới thiệu về machine learning không?"},
            {"role": "user", "content": "Cảm ơn, rất hữu ích!"},
            {"role": "user", "content": "Tôi đang học Python ở trường đại học."},
        ],
        "test_turn": {"role": "user", "content": "Bạn có nhớ tên tôi không?"},
        "expected_keyword": "Linh",
        "description": "Agent should recall user name after several unrelated turns.",
    },
    {
        "id": 2,
        "name": "Allergy conflict update",
        "group": "conflict_update",
        "setup_turns": [
            {"role": "user", "content": "Tôi dị ứng sữa bò."},
            {"role": "user", "content": "Bạn gợi ý bữa sáng phù hợp cho tôi nhé."},
        ],
        "test_turn": {"role": "user", "content": "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò. Tôi dị ứng gì vậy?"},
        "expected_keyword": "đậu nành",
        "description": "Agent must update allergy fact (recency wins) and confirm the correction.",
    },
    {
        "id": 3,
        "name": "Programming language preference",
        "group": "profile_recall",
        "setup_turns": [
            {"role": "user", "content": "Tôi rất thích Python và không thích Java."},
            {"role": "user", "content": "Tôi cần tìm hiểu về web framework."},
        ],
        "test_turn": {"role": "user", "content": "Gợi ý cho tôi một web framework phù hợp."},
        "expected_keyword": "Python",
        "description": "Agent should recommend Python-based framework knowing user preference.",
    },
    {
        "id": 4,
        "name": "Recall previous debug lesson",
        "group": "episodic_recall",
        "setup_turns": [
            {"role": "user", "content": "Hôm trước tôi bị lỗi kết nối Docker container, cuối cùng phải dùng docker service name thay vì localhost."},
            {"role": "user", "content": "Bài học là luôn dùng service name trong Docker Compose."},
        ],
        "test_turn": {"role": "user", "content": "Tôi lại bị lỗi kết nối trong Docker, bạn có nhớ kinh nghiệm trước đó không?"},
        "expected_keyword": "service name",
        "description": "Agent recalls Docker debugging episode from earlier in the session.",
    },
    {
        "id": 5,
        "name": "Learning style preference",
        "group": "profile_recall",
        "setup_turns": [
            {"role": "user", "content": "Tôi thích học kiểu hands-on, không thích đọc lý thuyết nhiều."},
            {"role": "user", "content": "Tôi đang học data science."},
        ],
        "test_turn": {"role": "user", "content": "Gợi ý cho tôi cách học deep learning hiệu quả."},
        "expected_keyword": "hands-on",
        "description": "Agent suggests hands-on approach based on stored learning preference.",
    },
    {
        "id": 6,
        "name": "FAQ knowledge retrieval — ML concept",
        "group": "semantic_retrieval",
        "setup_turns": [
            {"role": "user", "content": "Tôi đang nghiên cứu về AI."},
        ],
        "test_turn": {"role": "user", "content": "Giải thích sự khác nhau giữa overfitting và underfitting."},
        "expected_keyword": "overfitting",
        "description": "Agent retrieves ML knowledge from semantic memory to explain concepts.",
    },
    {
        "id": 7,
        "name": "Docker guide retrieval",
        "group": "semantic_retrieval",
        "setup_turns": [
            {"role": "user", "content": "Tôi cần deploy ứng dụng bằng Docker."},
        ],
        "test_turn": {"role": "user", "content": "Làm sao để các container trong Docker Compose kết nối với nhau?"},
        "expected_keyword": "service",
        "description": "Agent retrieves Docker networking info from semantic memory.",
    },
    {
        "id": 8,
        "name": "Token budget trimming (long conversation)",
        "group": "trim_budget",
        "setup_turns": [
            {"role": "user", "content": "Hãy giải thích chi tiết về neural networks."},
            {"role": "user", "content": "Tiếp tục giải thích về backpropagation."},
            {"role": "user", "content": "Gradient descent hoạt động thế nào?"},
            {"role": "user", "content": "Batch normalization là gì?"},
            {"role": "user", "content": "Dropout regularization hoạt động ra sao?"},
            {"role": "user", "content": "So sánh Adam và SGD optimizer."},
            {"role": "user", "content": "Transfer learning là gì?"},
        ],
        "test_turn": {"role": "user", "content": "Tóm tắt lại những gì chúng ta đã thảo luận."},
        "expected_keyword": "neural",
        "description": "Agent handles long conversation with token budget management.",
    },
    {
        "id": 9,
        "name": "Multi-fact profile update",
        "group": "conflict_update",
        "setup_turns": [
            {"role": "user", "content": "Tôi tên Minh, 25 tuổi, sống ở Hà Nội."},
            {"role": "user", "content": "Tôi làm software engineer ở FPT."},
            {"role": "user", "content": "À không, tôi vừa chuyển sang VinAI rồi."},
        ],
        "test_turn": {"role": "user", "content": "Bạn nhớ gì về tôi?"},
        "expected_keyword": "VinAI",
        "description": "Agent updates workplace fact (FPT → VinAI) and recalls all other facts.",
    },
    {
        "id": 10,
        "name": "Cross-session episodic recall",
        "group": "episodic_recall",
        "setup_turns": [
            {"role": "user", "content": "Tôi vừa hoàn thành project API Gateway, dùng FastAPI và đã deploy thành công lên Railway."},
            {"role": "user", "content": "Bài học lớn nhất là cần setup health check endpoint trước khi deploy."},
        ],
        "test_turn": {"role": "user", "content": "Tôi sắp deploy project mới, bạn có nhớ kinh nghiệm deploy trước đó của tôi không?"},
        "expected_keyword": "health check",
        "description": "Agent recalls deployment episode and lessons learned.",
    },
]

def run_single_conversation(graph, router, scenario: dict, use_memory: bool) -> dict:
    """Run a single multi-turn conversation and return the result."""
    messages = []
    all_responses = []
    user_id = f"bench_{scenario['id']}"

    if use_memory and router:
        router.short_term.clear()

    # Run setup turns
    for turn in scenario["setup_turns"]:
        messages.append(turn)
        if use_memory and router:
            router.short_term.store("msg", turn)

        state = {
            "messages": list(messages),
            "current_query": turn["content"],
            "user_id": user_id,
            "user_profile": {},
            "episodes": [],
            "semantic_hits": [],
            "memory_budget": MEMORY_TOKEN_BUDGET,
            "response": "",
            "token_usage": {},
        }
        result = graph.invoke(state)
        resp = result.get("response", "")
        messages.append({"role": "assistant", "content": resp})
        all_responses.append(resp)

    # Run test turn
    test_turn = scenario["test_turn"]
    messages.append(test_turn)
    if use_memory and router:
        router.short_term.store("msg", test_turn)

    state = {
        "messages": list(messages),
        "current_query": test_turn["content"],
        "user_id": user_id,
        "user_profile": {},
        "episodes": [],
        "semantic_hits": [],
        "memory_budget": MEMORY_TOKEN_BUDGET,
        "response": "",
        "token_usage": {},
    }
    result = graph.invoke(state)
    final_response = result.get("response", "")
    token_usage = result.get("token_usage", {})

    keyword = scenario["expected_keyword"].lower()
    passed = keyword in final_response.lower()

    return {
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "group": scenario["group"],
        "final_response": final_response,
        "expected_keyword": scenario["expected_keyword"],
        "passed": passed,
        "total_turns": len(scenario["setup_turns"]) + 1,
        "token_usage": token_usage,
    }

def generate_benchmark_md(results_memory, results_no_memory) -> str:
    """Generate the BENCHMARK.md content."""
    lines = []
    lines.append("# BENCHMARK.md — Lab #17: Multi-Memory Agent Benchmark Report\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    # Summary table
    lines.append("## 1. Benchmark Summary — 10 Multi-Turn Conversations\n")
    lines.append("| # | Scenario | Group | Turns | No-Memory Result | With-Memory Result | Pass? |")
    lines.append("|---|----------|-------|------:|------------------|-------------------|-------|")
    for rm, rnm in zip(results_memory, results_no_memory):
        no_mem_short = rnm["final_response"][:60].replace("|", "/").replace("\n", " ")
        with_mem_short = rm["final_response"][:60].replace("|", "/").replace("\n", " ")
        status = "Pass" if rm["passed"] else "Fail"
        lines.append(f"| {rm['scenario_id']} | {rm['scenario_name']} | {rm['group']} | {rm['total_turns']} | {no_mem_short}... | {with_mem_short}... | {status} |")
    lines.append("")

    # Pass rate
    passed = sum(1 for r in results_memory if r["passed"])
    lines.append(f"**Overall Pass Rate:** {passed}/{len(results_memory)} ({passed/len(results_memory)*100:.0f}%)\n")

    # Detailed results
    lines.append("---\n")
    lines.append("## 2. Detailed Conversation Transcripts\n")
    for i, (rm, rnm) in enumerate(zip(results_memory, results_no_memory)):
        sc = SCENARIOS[i]
        lines.append(f"### Scenario {sc['id']}: {sc['name']}")
        lines.append(f"**Group:** {sc['group']} | **Turns:** {rm['total_turns']} | **Expected keyword:** `{sc['expected_keyword']}`\n")
        lines.append(f"**Description:** {sc['description']}\n")
        lines.append("**Setup turns:**")
        for t in sc["setup_turns"]:
            lines.append(f"- User: {t['content']}")
        lines.append(f"\n**Test turn:** {sc['test_turn']['content']}\n")
        lines.append(f"**No-memory response:**\n> {rnm['final_response'][:300]}\n")
        lines.append(f"**With-memory response:**\n> {rm['final_response'][:300]}\n")
        lines.append(f"**Result:** {'PASS' if rm['passed'] else 'FAIL'} (keyword `{sc['expected_keyword']}` {'found' if rm['passed'] else 'not found'})\n")

    # Token analysis
    lines.append("---\n")
    lines.append("## 3. Token Usage Analysis\n")
    lines.append("| # | Scenario | No-Memory Tokens | With-Memory Tokens | Difference |")
    lines.append("|---|----------|----------------:|-----------------:|----------:|")
    for rm, rnm in zip(results_memory, results_no_memory):
        nm_tok = rnm["token_usage"].get("total_tokens", 0)
        wm_tok = rm["token_usage"].get("total_tokens", 0)
        diff = wm_tok - nm_tok
        lines.append(f"| {rm['scenario_id']} | {rm['scenario_name']} | {nm_tok} | {wm_tok} | +{diff} |")
    lines.append("")

    # Test group coverage
    lines.append("---\n")
    lines.append("## 4. Test Group Coverage\n")
    groups = {}
    for r in results_memory:
        g = r["group"]
        if g not in groups:
            groups[g] = {"total": 0, "passed": 0}
        groups[g]["total"] += 1
        if r["passed"]:
            groups[g]["passed"] += 1
    lines.append("| Test Group | Scenarios | Passed | Rate |")
    lines.append("|------------|----------:|-------:|-----:|")
    for g, stats in groups.items():
        rate = stats["passed"] / stats["total"] * 100
        lines.append(f"| {g} | {stats['total']} | {stats['passed']} | {rate:.0f}% |")
    lines.append("")

    # Reflection
    lines.append("---\n")
    lines.append("## 5. Reflection — Privacy & Limitations\n")
    lines.append("### 5.1 PII/Privacy Risks\n")
    lines.append("1. **Long-term Profile Memory** stores personally identifiable information (PII) directly:")
    lines.append("   - User name, age, location, workplace, allergies, preferences")
    lines.append("   - This is the **most sensitive memory type** because it contains explicit identity data")
    lines.append("2. **Episodic Memory** may inadvertently store sensitive task details (e.g., proprietary code, internal system names)")
    lines.append("3. **Semantic Memory** risk is lower since it stores domain knowledge, not user data\n")
    lines.append("### 5.2 Most Sensitive Memory\n")
    lines.append("**Long-term Profile Memory** is the most sensitive because:")
    lines.append("- Contains direct PII (name, location, health data like allergies)")
    lines.append("- Persists across sessions (long-lived)")
    lines.append("- If breached, provides a complete user profile that can be used for identity theft\n")
    lines.append("### 5.3 Deletion, TTL, and Consent\n")
    lines.append("Our implementation supports **GDPR right-to-be-forgotten**:")
    lines.append("- Each memory backend has a `delete(user_id)` method")
    lines.append("- To fully delete a user's data, all 4 backends must be cleared:")
    lines.append("  - `short_term.clear()` — removes conversation buffer")
    lines.append("  - `long_term.delete(user_id)` — removes profile JSON file")
    lines.append("  - `episodic.delete(user_id)` — removes episode JSONL file")
    lines.append("  - `semantic.delete(source)` — removes user-contributed knowledge")
    lines.append("- **Recommended TTL policy:**")
    lines.append("  - Profile preferences: 90 days")
    lines.append("  - Profile facts: 30 days")
    lines.append("  - Episodes: 7 days")
    lines.append("  - Short-term: session-only (auto-cleared)")
    lines.append("- **Consent**: Agent should explicitly ask user before storing PII (opt-in model)\n")
    lines.append("### 5.4 Technical Limitations\n")
    lines.append("1. **LLM Fact Extraction Accuracy**: The LLM-based extractor may miss implicit facts or hallucinate facts not stated by the user. JSON parsing can fail on malformed LLM output.")
    lines.append("2. **Semantic Search Quality**: Depends on embedding model quality. Short or ambiguous queries may retrieve irrelevant chunks. No re-ranking mechanism.")
    lines.append("3. **No Real-time Sync**: Multiple agent instances cannot share memory state in real-time (no pub/sub). Dict-based profile store is single-process only.")
    lines.append("4. **Token Budget Estimation**: tiktoken provides accurate counts for OpenAI models but the budget allocation between memory types is static (not adaptive).")
    lines.append("5. **Episodic Retrieval**: Keyword-based matching is simplistic compared to embedding-based similarity. May miss semantically related but lexically different episodes.")
    lines.append("6. **Conflict Resolution**: Simple recency-wins policy may be too aggressive — no user confirmation before overwriting important facts (e.g., medical data).")
    lines.append("7. **Scale Limitations**: JSON/JSONL persistence does not scale beyond ~10K users. Production deployment would need Redis + PostgreSQL.\n")
    lines.append("### 5.5 What Would Help Most?\n")
    lines.append("- **Long-term profile** helps the agent the most — it enables personalization without repeating preferences each session")
    lines.append("- **Episodic memory** has the highest risk if retrieved incorrectly — wrong past experience could lead to incorrect advice")
    lines.append("- **Federated forgetting** is needed in multi-agent systems — deletion must propagate to all agents with a copy of the data\n")

    return "\n".join(lines)

def main():
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY not set.")
        sys.exit(1)

    print("=" * 60)
    print("  Benchmark Runner — 10 Multi-Turn Conversations")
    print("=" * 60)

    # Build graphs
    print("\n[1/4] Building memory agent graph...")
    memory_graph, router = build_memory_agent_graph(ingest_knowledge=True)
    print("[2/4] Building no-memory baseline graph...")
    no_memory_graph = build_no_memory_agent_graph()

    # Run benchmarks
    results_memory = []
    results_no_memory = []

    for i, scenario in enumerate(SCENARIOS):
        print(f"\n[3/4] Running scenario {scenario['id']}/10: {scenario['name']}...")

        # Run with memory
        print(f"  -> With memory...", end=" ", flush=True)
        t0 = time.time()
        try:
            rm = run_single_conversation(memory_graph, router, scenario, use_memory=True)
            print(f"{'PASS' if rm['passed'] else 'FAIL'} ({time.time()-t0:.1f}s)")
            results_memory.append(rm)
        except Exception as e:
            print(f"ERROR: {e}")
            results_memory.append({
                "scenario_id": scenario["id"], "scenario_name": scenario["name"],
                "group": scenario["group"], "final_response": f"Error: {e}",
                "expected_keyword": scenario["expected_keyword"], "passed": False,
                "total_turns": len(scenario["setup_turns"]) + 1, "token_usage": {},
            })

        # Run without memory
        print(f"  -> No memory...", end=" ", flush=True)
        t0 = time.time()
        try:
            rnm = run_single_conversation(no_memory_graph, None, scenario, use_memory=False)
            print(f"{'PASS' if rnm['passed'] else 'FAIL'} ({time.time()-t0:.1f}s)")
            results_no_memory.append(rnm)
        except Exception as e:
            print(f"ERROR: {e}")
            results_no_memory.append({
                "scenario_id": scenario["id"], "scenario_name": scenario["name"],
                "group": scenario["group"], "final_response": f"Error: {e}",
                "expected_keyword": scenario["expected_keyword"], "passed": False,
                "total_turns": len(scenario["setup_turns"]) + 1, "token_usage": {},
            })

    # Generate report
    print("\n[4/4] Generating BENCHMARK.md...")
    report = generate_benchmark_md(results_memory, results_no_memory)
    output_path = PROJECT_ROOT / "BENCHMARK.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {output_path}")

    # Summary
    passed = sum(1 for r in results_memory if r["passed"])
    print(f"\nResults: {passed}/{len(results_memory)} scenarios passed with memory")
    print("Done!")

if __name__ == "__main__":
    main()
