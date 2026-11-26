---
name: memprompt
description: >-
  Build a prompt for a downstream GENERATION tool (Claude Design, image
  generators, UI/front-end builders like v0, etc.) by SUMMARIZING Zach's own
  ideas plus the decisions he explicitly accepted with an orchestrator - pulled
  from native Codex memory, durable project records, and historical conversations
  (verbatim where possible). Use whenever Zach
  says "make a prompt from memory", "turn my idea into a prompt for a tool",
  "give me a prompt for Claude Design", "rewrite that prompt", or otherwise wants
  to feed his vision to a creative/generation tool. CRITICAL: this skill does NOT
  invent design specifics - the generation tool gets the creative freedom.
---

# memprompt - a prompt FROM durable intent, not from your imagination

Zach hands his vision to a generation tool (Claude Design, an image model, a UI
builder). The prompt's ONLY job is to faithfully convey **what Zach said** and
**what Zach explicitly accepted with an orchestrator** - then get out of the way so the tool's
own creativity does the actual design.

## The cardinal rule - DO NOT OVER-CONSTRAIN

The #1 failure mode (Zach has called this out explicitly): the LLM inserts design
decisions **Zach never made** - exact colors ("this should be electric blue"),
counts ("24 neurons"), named effects ("a ripple ring + pulse"), precise layouts,
typography, motion specifics. That is **not your job**. It is the generation
tool's job, and over-constraining it is exactly what makes the output worse. A
generation tool needs creative latitude to be good.

- INCLUDE only: what Zach explicitly said + decisions he explicitly accepted
  + the real hard constraints he actually stated.
- EXCLUDE: every aesthetic/implementation specific he did NOT state - palette,
  exact numbers, named effects, exact panel layouts, fonts, motion details.
  Hand those to the tool via an explicit "creative freedom" clause.
- If unsure whether Zach said it: **leave it out** (or list it as an open option
  for the tool to decide). Never assert a preference he didn't voice.
- You are a SUMMARIZER, not a designer.

## Method

1. **Gather his actual words + decisions from memory:**
   - Native Codex memory under `~/.codex/memories/`, the active
     obligation board, and relevant repo decision/spec files.
   - The historical Claude intent ledger - `memory/intent/topics/*.md` (consolidated, status-tagged)
     and especially `memory/intent/archive/*.md` (VERBATIM session captures: the
     best source for his exact phrasing).
   - If needed, search archived conversations / session transcripts for his
     original verbatim descriptions of the thing.
2. **Sort what you found into buckets:**
   - **Context** - what the thing is, in a line or two.
   - **Zach's goals / ideas** - his stated wants. Quote verbatim where the wording
     is strong; otherwise paraphrase concisely. Keep his voice ("I want...").
   - **Decisions we locked together** - things Zach explicitly accepted in conversation;
     mark them as settled.
   - **Hard constraints** - only ones he actually stated (e.g. "must be embedded
     in the app", "keep the real graph engine, don't rebuild it").
   - **Creative freedom (the tool's job)** - an explicit, named list of what is
     intentionally left open: "you choose the palette, layout, composition, motion,
     and the exact look; surprise me; make it genuinely premium."
3. **Write the prompt** in that order, tight, in his voice. Prefer his words to yours.
4. **Output** just the prompt as a finished reusable writing artifact, then ONE line
   naming what you deliberately left to the tool's creative freedom.

## When the target is improving an EXISTING build (not from scratch)

Say so up front in the prompt: "This is an IMPROVEMENT pass on an existing,
already-built surface - use the linked codebase's real components/tokens; raise
quality and fold in the ideas below; do NOT rebuild from zero."

## Don'ts

- Don't add a single color, count, or named effect Zach didn't say.
- Don't turn his rough idea into your detailed spec.
- Don't pad or pre-empt the tool's creativity. Summarize his intent; stop there.
