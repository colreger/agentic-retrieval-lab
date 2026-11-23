# Research status — 23 November 2026

This summary reconciles the public code with the latest thesis formulation in
the project conversation “MASTERARBEIT: Thema und Gliederung schreiben”. It does
not publish the private thesis manuscript or invent additional experiment runs.

## Latest research question

How do Nemotron and JEV differ in retrieval quality and end-to-end latency when
they iteratively choose search steps based on evidence in the current passages?

The proposed comparison holds the initial retrieval, context preparation rules,
available tools and intervention limit constant. Each model can keep the current
selection, re-rank candidates, rewrite and retrieve again, or rewrite, retrieve
and re-rank. After an intervention it observes the updated result before its
next decision. The planned maximum is two interventions.

This is “agentic” in a bounded sense: the model selects actions from the current
search state; the application controls the tools and stopping rules. It is not
an unrestricted autonomous agent.

## Evaluation plan

The planned dataset is the BEIR version of Natural Questions. BEIR is
**Benchmarking-IR**, where IR means Information Retrieval, as introduced in the
[original benchmark paper](https://arxiv.org/abs/2104.08663); the
dataset name Natural Questions refers to naturally occurring user questions.
Passage boundaries stay fixed across strategies.

- **Hit@5:** whether at least one annotated relevant passage appears in the final
  five results. Report recovered and lost hits separately.
- **MRR@5, Mean Reciprocal Rank at 5:** the reciprocal rank of the first relevant
  result in the first five, averaged over questions; zero when none is found.
- **Candidate-pool failures:** no annotated relevant passage in the pool.
- **Ranking failures:** a relevant candidate exists but falls below the output's
  top five. This classification depends on the pool size.
- **End-to-end latency:** initial retrieval, every controller decision and every
  executed recovery step, ending at the final passage list. Report median and
  p95 (95th percentile), plus action counts and failures.

The study ends at passage selection. Retrieval relevance labels do not establish
that the passages fully answer every part of the question, or that a generator
would produce a correct answer. No answer-generation quality score is claimed.

## What is already implemented and measured

`routing.py` validates a single selected action, applies a time budget and checks
the returned five unique passage identifiers. The offline demo uses scripted
decisions and synthetic rankings. It does not run the proposed iterative study.

The README's historical fixed-strategy and binary-router tables remain labeled
as development results. Their controlled gold-enriched corpus and estimated
component-based latency must not be presented as a full-corpus, held-out,
end-to-end result for the new iterative policy. No new iterative benchmark
numbers were found in the latest thesis formulation.

Next implementation/evaluation work is to make the two-intervention loop and
updated-state feedback explicit, then execute the matched comparison and audit
per-question rankings, stopping decisions, failures and measured total latency.
