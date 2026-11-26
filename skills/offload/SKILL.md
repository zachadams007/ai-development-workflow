---
name: offload
description: Run a self-contained, fully specified worker task on an exact Codex, Cursor, or Claude model while the calling orchestrator retains ownership and verification. Use automatically for model-agnostic mechanical work, deterministic transformations, extraction, boilerplate, or a task with a verified specialist-model advantage; use only after architecture/taste/scoring decisions are locked. Enforces an explicit caller, target, model, effort, mode, and absolute folder. Never treat dispatch or exit success as completion, and fall back to Cursor GUI automation when the headless Cursor Agent cannot honor exact routing.
---

# Offload

Offload execution, not judgment or accountability. The caller owns scope, monitoring, integration, and final verification.

## Eligibility

Use when the task is:

- self-contained and completely specified;
- safe to run in an isolated folder/worktree;
- mechanical or model-agnostic, or there is a verified specialist advantage;
- independently verifiable with a diff, artifact, tests, or runtime behavior.

Keep architecture, unresolved product/design taste, scoring/ranking/personalization, novel synthesis, and final acceptance in the orchestrating session on a deep-tier model unless a current specialist is demonstrably better.

## Routing

Verify the live roster first when it may have changed.

- **Codex Luna medium/high:** deterministic extraction, formatting, indexing, repetitive edits, test-fix loops.
- **Codex Terra high/xhigh:** substantial implementation/research/debugging that still needs judgment.
- **Cursor Auto/Composer:** pre-scoped in-editor work. Current reliable path on this Windows machine is GUI automation because `cursor-agent` is not installed.
- **Specific Cursor/Claude model:** only for a current verified task advantage; state the reason.

For every worker state exact caller, target, model, effort/mode, and absolute
folder/worktree. Never offload back to the caller's own provider family; use its
native task/subagent surface for same-provider fan-out.

## Worker packet

Include outcome, context/files to read, exact scope and exclusions, acceptance criteria, verification, evidence format, and prohibitions on secrets/destructive actions/push/deploy/message sending unless separately authorized. Tell the worker to report blockers with evidence and stop after its lane.

## CLI runner

```powershell
$prompt | python ~/.agents/skills/offload/offload.py `
  --caller codex --target claude --mode execute `
  --model claude-opus-4-8 --effort high `
  --cd C:/absolute/worktree
```

For Codex from a non-Codex caller, make the sandbox explicit:

```powershell
$prompt | python ~/.agents/skills/offload/offload.py `
  --caller claude --target codex --mode execute `
  --model gpt-5.6-luna --effort medium `
  --cd C:/absolute/worktree --sandbox workspace-write
```

Targets:

- `codex`: exact model, effort, folder, and sandbox are required; generate mode
  additionally requires `--sandbox read-only`; execute mode must use an isolated
  worktree for concurrent edits.
- `cursor`: headless execution is rejected until the installed CLI can prove
  exact model and effort/mode routing. Use live Cursor GUI automation or another
  target; a missing CLI returns 127 with that fallback.
- `claude`: exact current model and supported effort are passed to the CLI;
  generate mode uses plan permissions and execute mode uses auto permissions.
  Blanket permission bypass is not used.

The runner rejects a caller/target family match before executable discovery.
This keeps self-targeting out of the generic subprocess path while native
provider task/subagent surfaces remain available for same-provider parallelism.

The runner is synchronous and is not an overnight job manager. For managed background work, use Codex task/subagent tools and `$delegate`; record task IDs and monitor them there.

## Cursor GUI fallback

1. Open the exact folder with `cursor -n "C:\absolute\worktree"`.
2. Use live computer control to confirm the folder and current model roster.
3. Select exact model and available effort/mode; paste the packet.
4. Monitor permission prompts and output. Cursor's broad permissions make isolation and prohibitions mandatory.
5. Inspect the diff and run verification independently from Codex; reprompt concrete failures.

## Completion

Exit code 0, a result event, a commit, or worker prose is provisional. The caller must inspect the actual artifact/diff, run the acceptance gates, use the real app when user-facing, and feed defects back into another pass. Record unfinished work on the active board with owner and trigger.
