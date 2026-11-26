---
name: research-coverage
description: Run broad, evidence-led, gap-checked research that goes beyond a normal web scan and ends in original synthesis. Use for hard or high-value domains, current tool/model/skill selection, competitive or technical landscape work, strategy research, requests to read every strong source, or any task where missing an important paper, book, article, transcript, GitHub repository, skill/plugin/MCP server, modern free tool/site, benchmark, or local prior experiment would materially reduce quality.
---

# Research Coverage

Produce decision-grade research with a visible coverage boundary and gap check. Do not claim "comprehensive" merely because several searches returned plausible sources.

## 1. Define the research contract

Write down:

- decision or system this research must improve;
- questions that must be answered, decomposed by the system's distinct concerns;
- explicit as-of timestamp and time/currentness boundary;
- inclusion and exclusion rules;
- operating definitions for ambiguous constraints such as "free," "local-first," "safe," or "production-ready";
- privacy/scope boundary for local memory, files, transcripts, and prior research;
- output and evidence required;
- what would change the recommendation.

Reuse relevant in-scope local research and memory first, then research the delta. Stop local-history exploration once it answers the current contract or yields no new decision-relevant evidence. Treat old conclusions as hypotheses when facts may have drifted.

## 2. Build the source-family matrix

Choose every family relevant to the decision:

1. Primary/official documentation, specifications, announcements, datasets, filings, and standards.
2. Peer-reviewed papers, strong preprints, benchmarks, replications, and failure analyses.
3. High-quality books, long-form technical or industry articles, and practitioner case studies when they add material evidence not already covered.
4. Talks, podcasts, courses, and quality YouTube transcripts when they add implementation detail, operational evidence, or a distinct perspective.
5. GitHub repositories, examples, issues, discussions, release histories, and maintained alternatives.
6. Skills, plugins, MCP servers, agent frameworks, model/tool catalogs, and workflow packages.
7. Modern free tools and websites that can materially replace manual work or unlock a new approach.
8. Community evidence only where it reveals real-world failure modes; label anecdotes as anecdotes.
9. Local files, logs, experiments, tests, transcripts, prior decisions, and observed app behavior.

Use [the coverage ledger template](references/coverage-ledger-template.md). Record reproducible queries/surfaces checked, source URL or local path, accessed date, evidence grade, independence/conflict, strong inclusions, exclusions with reasons, and unresolved access gaps. Do not fill a family for checklist completeness when it is immaterial; mark it not material and explain why.

For technical questions, prefer primary sources. For current claims, verify publication date and the date the underlying event or release occurred. For books/videos behind access barriers, search legitimate summaries, author materials, papers, excerpts, or transcripts; record what could not be verified.

## 3. Search in widening rings

Run discovery in parallel where possible:

- obvious canonical terms and primary sources;
- synonyms, adjacent fields, competing architectures, and negative results;
- cited-by/reference chains and the maintainers/authors behind the best sources;
- current GitHub/skill/plugin/tool ecosystems;
- adversarial queries such as failures, limitations, abandoned approaches, security, bias, and benchmark criticism.

Maintain a compact query/discovery log so late discoveries and deduplication decisions are reproducible. De-duplicate near-identical summaries. Prefer source diversity over ten articles repeating one press release.

Do not stop at the first viable tool. Compare the strongest alternatives using criteria tied to the actual project: capability, evidence, maintenance, integration burden, license, privacy/security, deletion and scope isolation, cost, latency, durability, and reversibility. For persistent-memory or agent systems, cover untrusted writes, poisoning, provenance, retention/erasure, and cross-project isolation even if the user did not name them.

## 4. Extract evidence, not bookmarks

For each included source, capture only decision-relevant evidence:

- claim or mechanism;
- strength/quality of evidence using an explicit grade (primary measured, primary descriptive, independent measured, independent descriptive, or anecdotal);
- source independence, incentives, and conflicts;
- constraints and failure modes;
- applicability to Zach's project;
- publication/event dates, accessed date, and maintenance state;
- conflicts with other evidence.

Distinguish facts, source opinions, Zach's decisions, and the orchestrator's proposals. Never record a proposed idea as agreed.

## 5. Synthesize beyond the sources

After evidence collection:

1. State the strongest current approach.
2. Identify assumptions shared by existing approaches.
3. Combine useful mechanisms across domains.
4. Propose at least one better or future-facing system when evidence supports it.
5. Define the smallest prototype or experiment that could falsify the new idea.
6. Compare expected upside, failure modes, cost, and reversibility.
7. State whether the recommendation is a turnkey product, a component, or a system architecture with replaceable parts.

The absence of an existing implementation is a research finding, not a prohibition. Separate "not yet demonstrated," "blocked by current access/resources," and "physically or logically impossible."

## 6. Run the gap check

Before finishing, ask:

- Which relevant source family is still empty, and why?
- Did any obvious current tool/model/repo/skill appear only after indirect discovery?
- Are the best claims supported by primary evidence?
- Did recency, paywalls, language, ranking bias, or search-engine bias hide alternatives?
- Did local prior work already disprove or constrain the recommendation?
- Were security, privacy, deletion, durability, and portability covered where persistent state is involved?
- Are memory quality, obligation completion, security, and recovery tested as separate outcomes rather than one vague score?
- What evidence would most likely overturn the conclusion?

Close each gap, document it as genuinely inaccessible/out of scope, or convert it into an active obligation with owner and trigger. Never bury the gap in memory alone.

## 7. Deliver

Lead with the recommendation, as-of date, and confidence. Include a compact coverage matrix, evidence grades, key contradictions, unresolved gaps, the original synthesis, and the next experiment. Cite sources at the claim they support. When research is part of an authorized build, update the active obligation board and feed the recommendation into the loop-engineering acceptance criteria. In read-only/report-only work, return the proposed board delta without editing it.

When adoption depends on a named operating system, runtime, device, account surface, or deployment target, label compatibility as `claimed` until observed there. Run the smallest safe local execution/restart/recovery test, or make the missing observation the recommendation's principal unresolved gap and next experiment.
