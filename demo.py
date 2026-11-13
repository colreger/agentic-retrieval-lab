"""Exercise the real routing guardrails on synthetic rankings, without network calls."""

from metrics import evaluate_ranking
from routing import guarded_route, routing_context


def main():
    baseline = ["a", "b", "c", "d", "e"]
    deeper = ["f", "g", "h", "i", "j"]
    documents = {
        doc_id: {"text": f"Synthetic passage {doc_id}"} for doc_id in baseline + deeper
    }
    state = routing_context(
        {"question": "Which passage contains the procedure?"},
        documents,
        {"top100": baseline + deeper},
        "top5-plus-6-10",
    )
    rankings = {
        "rerank50": ["f", "a", "b", "c", "d"],
        "rewrite": ["k", "a", "b", "c", "d"],
        "combined50": ["k", "f", "a", "b", "c"],
    }
    scenarios = [
        ("Keep baseline", "minilm", ["a"]),
        ("Recover with re-ranking", "rerank50", ["f"]),
        ("Recover with rewriting", "rewrite", ["k"]),
        ("Combine both actions", "combined50", ["k"]),
        ("Regression after re-ranking", "rerank50", ["e"]),
        ("Reject unknown action", "unsupported", ["a"]),
    ]
    print(f"{'Scenario':31} {'Action':12} {'Hit@5':8} Outcome")
    for name, proposal, gold in scenarios:
        final, route = guarded_route(
            state,
            lambda _state, _timeout: proposal,
            lambda action, _remaining: rankings[action],
            baseline,
            timeout_seconds=1,
        )
        before = evaluate_ranking(baseline, gold)["hit_at_5"]
        after = evaluate_ranking(final, gold)["hit_at_5"]
        outcome = {1: "recovery", 0: "unchanged", -1: "regression"}[after - before]
        print(f"{name:31} {route.action:12} {before} -> {after}   {route.fallback_reason or outcome}")


if __name__ == "__main__":
    main()
