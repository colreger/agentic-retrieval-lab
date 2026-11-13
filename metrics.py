"""Ranking metrics used by the thesis development benchmark."""

import math


def evaluate_ranking(ranked, gold):
    gold = set(gold)
    if not gold or len(ranked) != len(set(ranked)):
        raise ValueError("Invalid ranking or labels")

    hits = [rank for rank, doc_id in enumerate(ranked[:5], 1) if doc_id in gold]
    dcg = sum(1 / math.log2(rank + 1) for rank in hits)
    ideal_dcg = sum(1 / math.log2(rank + 1) for rank in range(1, min(5, len(gold)) + 1))
    return {
        "hit_at_5": int(bool(hits)),
        "recall_at_5": len(hits) / len(gold),
        "reciprocal_rank_at_5": 1 / hits[0] if hits else 0.0,
        "ndcg_at_5": dcg / ideal_dcg,
    }
