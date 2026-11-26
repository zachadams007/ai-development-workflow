---
name: handoff
description: Lossless session/task handoff between any tools (Claude, Codex, Cursor). Invoke as $handoff standalone or at the end of a message when a fresh orchestrator task is genuinely useful, an interruption/usage boundary requires transfer, or work must move to another folder/host/model. Reconciles the full obligation ledger, preserves pending instructions at high fidelity, recommends the exact current model, effort, and absolute folder/worktree, creates or steers the successor task directly when authorized and tools are available, and saves a durable backup so Zach never has to reconstruct context.
---

# Handoff

Transfer the work without transferring ownership back to Zach.

## 1. Finish cheap critical work first

If the triggering message contains quick safe actions (memory note, board update, status check, one-line fix), complete them before the handoff. Do not start a large new lane merely to avoid handing it off.

## 2. Reconcile state

Compile from the conversation, active board, goal, task/thread statuses, repo instructions, git state, runtime evidence, and relevant memory:

- mission and observable done condition;
- completed work with evidence;
- in-flight workers/tasks with IDs, model/effort/folder, and exact state;
- every pending instruction from Zach's latest message (verbatim or near-verbatim);
- prior open obligations and priority;
- locked decisions vs orchestrator proposals;
- discoveries, failures, gotchas, and sensitive-action boundaries;
- branch/commit/dirty files/running services;
- files and evidence to read first;
- questions truly requiring Zach;
- immediate first moves.

Compare the source message line-by-line with the obligation ledger. Nothing may disappear merely because the new task will have memory.

## 3. Choose the destination

Recommend all three explicitly:

- **Model:** deep tier for the next orchestrator (e.g. Claude Opus 5 at high/max); balanced tier for a bounded worker; mechanical tier for deterministic work. Name the exact current model, and prefer the tool that has usage headroom.
- **Effort:** Sol max for hard single-agent judgment, Sol Ultra for root-level parallel decomposition, Terra high/xhigh, or Luna medium/high.
- **Folder/worktree:** exact absolute path and branch/environment.

Verify the current model roster when it may have changed. Claude or a Cursor specialist model is recommended only when a current, task-specific advantage is verified and explained.

When Zach explicitly asks for a new/background task and the Codex task tools are available, create or steer the task directly with the selected model/effort/folder. Do not make Zach copy a prompt solely because that was the Claude-era workflow. Still provide the complete packet inline as the durable/auditable artifact.

## 4. Produce the packet

Use this structure:

```text
# Handoff: <title>
Date: <date>
Destination model: <exact model>
Reasoning effort/mode: <exact effort>
Folder/worktree: <absolute path>
Branch/starting state: <exact state>

## Objective and done condition
<1-3 sentences>

## Read first
<ordered local files, task/thread IDs, and evidence>

## Verified completed work
<outcome + commit/test/runtime evidence>

## In flight
<worker/task ID, exact model/effort/folder, current state, next check>

## Pending instructions from Zach
<verbatim or near-verbatim, no detail loss>

## Other active obligations
<priority, owner, trigger, acceptance>

## Locked decisions
<do not relitigate>

## Proposals not yet decided
<clearly labeled as proposals>

## Gotchas and boundaries
<failures, collisions, secrets/sensitive actions, environment quirks>

## Git/runtime state
<branch, commit, dirty files, servers/apps>

## Immediate moves
1. ...
2. ...
3. ...

## Verification and closure
<commands, live app behaviors, board/goal updates required>
```

The packet must be self-contained enough for a cold task, while pointing to exact high-fidelity source files rather than bloating with irrelevant history.

## 5. Save and wire it

Save a backup under the relevant repo's `docs/handoffs/` when that convention exists; otherwise use `~/.codex/handoffs/handoff-<YYYY-MM-DD-HHMM>.md`. Put the destination task ID and handoff path on `~/workspace/ORCHESTRATION-BOARD.md`.

If a new Codex task was created, monitor until it has actually received/started the packet. A created task chip or sent message is not evidence the lane is progressing.

## 6. Stop conditions

After a true session-ending handoff, do not start unrelated new work in the old task. Mark every unfinished item as owned by the destination with a next trigger. If no new task was requested/created, give the packet to Zach inline, but still preserve it locally and state exact model/effort/folder.

## Anti-patterns

- Do not say "open Claude" by default.
- Do not omit the model, effort, or folder.
- Do not summarize away Zach's pending instructions.
- Do not call an in-flight task complete.
- Do not make memory the only transfer surface.
- Do not record orchestrator suggestions as Zach's decisions.
