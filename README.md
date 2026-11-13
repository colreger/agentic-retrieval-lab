# Agentic Retrieval Lab

Agentic routing and retrieval evaluation for RAG with Nemotron and JEV (System One).

**Planned GitHub repository name:** `agentic-retrieval-lab`

Can a router recover missing evidence while sending fewer queries through an expensive re-ranker? This portfolio project extracts the routing logic and development findings from an ongoing master's thesis.

## Run the offline demo

From the repository root, run with Python 3.10 or newer:

```bash
python3 demo.py
```

The demo runs the thesis routing guardrails on synthetic rankings with scripted decisions. It exercises all four actions, a recovery, a regression, and a fallback to the baseline for an invalid decision. It uses the Python standard library and runs offline.

The portfolio code includes the routing logic, provider adapters, and ranking metrics. The original thesis repository contains the retrieval and model execution pipelines, benchmark scripts, and the Retrieval Lab interface.

## How routing works

1. Retrieve an initial ranking. Build a routing context from the question and the top five passages, optionally adding short excerpts from ranks 6–10.
2. Ask Nemotron or JEV to choose one action: keep the current results, re-rank 50 candidates, rewrite and search again, or rewrite, search and re-rank.
3. Validate the action, run it within the remaining time budget, and verify that the result contains five unique passage IDs. Return the original top five on a handled error, invalid output, or missed deadline.

[routing.py](routing.py) contains the guardrails and the provider adapters from the thesis code. The adapters send the question and passage excerpts to the selected provider. The executor is supplied by the caller. Deadline checks discard late results, and execution depends on the caller honoring the remaining budget.

## Development results

The fixed-strategy benchmark used 1,000 questions and a controlled, gold-enriched pool of 21,220 passages from Natural Questions. MiniLM achieved **91.5% Hit@5**. Re-ranking 50 candidates raised it to **93.9%**, recovering 37 misses and losing 13 baseline hits. Hit@5 counts questions with at least one labeled evidence passage among the first five results.

A follow-up on 1,000 questions used a binary router to decide whether to keep the baseline or re-rank 50 candidates. It combined recorded router decisions with archived retrieval rankings.

| Strategy | Hit@5 | Re-ranked queries | Estimated p95 |
| --- | ---: | ---: | ---: |
| MiniLM baseline | 90.0% | 0 | 8 ms |
| Always re-rank | 92.6% | 1,000 | 288 ms |
| Nemotron-gated re-ranking | 92.9% | 384 | 589 ms |
| JEV-gated re-ranking | 93.1% | 327 | 581 ms |

Both routers reduced the number of queries re-ranked. Adding a model call for every question increased estimated p95. The latency estimates sum recorded component timings per question. The Hit@5 differences are descriptive for this development run.

The offline demo exercises the newer four-action policy. The table reports the earlier binary policy. A held-out, end-to-end comparison of the four-action policy is planned. The historical results above come from the thesis benchmark archives. This portfolio copy includes synthetic demo inputs.
