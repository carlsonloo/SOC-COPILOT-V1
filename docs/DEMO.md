# SOC Copilot V1 Demo Guide

This guide is designed for a five-minute portfolio or interview walkthrough.

## 1. Prepare

From the repository root:

```bash
python --version
python -m pip install -r requirements.txt
```

Use Python 3.10 or newer. The project has no third-party runtime dependencies.

## 2. Prove the baseline

```bash
python tests.py
```

Point out these results:

- Three deterministic scoring cases pass.
- The initial `40 / Medium` assessment remains unchanged after new evidence arrives.
- The updated assessment becomes `65 / High`.
- Retrieval includes `SL-001` and `SL-002`, while excluding retired or irrelevant chunks.
- The recommendation is traceable to policy chunk IDs and requires human review.
- Analyst feedback and the end-to-end orchestration tests pass.

## 3. Run the product flow

```bash
python demo.py
```

Walk through the JSON output in this order:

1. `risk_assessment`: deterministic score, severity, ruleset version, time and evidence snapshot.
2. `summary`: human-readable explanation derived from the approved assessment.
3. `recommendation`: policy-grounded guidance with `supported_by` provenance.
4. `human_review_required`: containment remains under analyst control.
5. `analyst_feedback`: the analyst modifies the proposal, records a reason and closes the incident as contained.

## 4. Suggested interview narrative

> I built a modular SOC Copilot that separates deterministic security decisions from generative explanation. Risk scoring is versioned and auditable, assessment history preserves point-in-time evidence, retrieval excludes retired or irrelevant policy, and recommendations cite their supporting chunks. High-impact containment remains human-controlled, and analyst modifications become evaluation data. V1 uses mock generation and metadata retrieval intentionally so the architecture and safety contracts can be tested before adding model and vector-database variability.

## 5. Be explicit about V1 limits

Do not describe this as production RAG or an autonomous SOC agent. V1 uses:

- in-memory fixtures rather than a database;
- deterministic mock text rather than a live LLM;
- metadata filtering rather than semantic or hybrid search;
- local assertions rather than a production evaluation platform;
- no authentication, authorization, API layer or durable audit store.

These are roadmap items, not hidden capabilities.
