---
name: delegate
description: Parallel delegation and obligation-management engine. Invoke as $delegate whenever Zach hands over multiple asks or a large context dump, explicitly requests delegation/background sessions/parallel lanes, or the work has three or more independent lanes or is likely to exceed one hour. Enumerates every obligation, builds a dependency graph, routes each lane to the current best model/tool with exact model, effort, and folder, dispatches independent work early, monitors and corrects every worker, verifies output and live behavior, and leaves no item buried in memory or non-terminal.
---

# Delegate

The session Zach is talking to remains the master context holder and final quality gate for this work, whichever tool it is. Delegate execution, never ownership.

## 1. Capture the complete obligation ledger

Before dispatching anything, extract every item from Zach's message, including side notes, future ideas, questions, constraints, quality expectations, and "while you're there" requests.

For each item record:

| Field | Required content |
|---|---|
| ID | Stable short ID |
| Source | Exact message/decision that created it |
| Deliverable | Observable result, not an activity |
| Status | queued / running / waiting / verifying / verified / obsolete / rejected |
| Owner/lane | Root, subagent, background task, Cursor, Claude, automation |
| Model | Exact current model ID or verified GUI model |
| Effort/mode | Exact reasoning effort or Cursor mode |
| Folder | Exact absolute folder/worktree |
| Dependencies | Items that must finish first |
| Acceptance | Tests, artifact, and live behavior required |
| Next trigger | Event/time/result that resumes it |
| Evidence | Thread/process ID, diff, test result, screenshot, or runtime observation |

Put unfinished durable obligations on `~/workspace/ORCHESTRATION-BOARD.md`. Memory may preserve context, but "saved to memory" is never a disposition.

## 2. Build the dependency graph

Classify each item:

- **Independent now:** dispatch immediately.
- **Depends on another lane:** queue with the exact trigger.
- **Root-only:** architecture, synthesis, taste Zach delegated, ranking/scoring/personalization, integration, or final acceptance.
- **Zach decision:** stop only if he explicitly wants to choose or the fork materially changes the product.
- **Sensitive action:** require explicit confirmation for destructive, financial, account, privacy/security, credential, irreversible, message-sending, push/deployment, or live-trade/order actions.

Batch questions at the first real decision boundary. Continue every safe independent lane while waiting.

## 3. Route by current capability

Verify live when the roster may have changed.

Route to a **tier**, then resolve the tier against the roster your tool actually lists right now. Check the model roster, authentication state, and remaining capacity before a long lane. Delegating a lane never moves master context, architecture, or final acceptance away from *this* session.

| Task shape | Tier | Current examples (reverify) |
|---|---|---|
| Main orchestration, novel system design, difficult diagnosis, final quality gate | Deep, high/max effort | Claude Opus 5; Codex top reasoning tier |
| Substantial research, implementation, independent debugging/review | Balanced, high effort | Claude Sonnet 5; Codex mid tier |
| Fully specified mechanical edits, extraction, formatting, indexing, test-fix loops | Mechanical | Claude Haiku 4.5; Codex light tier; Cursor Auto |
| Pre-scoped in-editor grunt | Mechanical | Cursor Auto/Composer through verified GUI automation |
| Task with a verified specialist advantage | Any | State the evidence and reason |

Keep the orchestrating session on the deep tier and delegate easier work. Never route from an old snapshot or a stale model name. Never use a parallelism-heavy child configuration when that child cannot spawn descendants.

## 4. Choose the execution surface

### Native subagents

Use in-task subagents for bounded, independent work when Zach or the governing instruction/skill has authorized delegation. The currently exposed spawn call does not pin model or effort, so do not claim it does. Give each subagent a concrete task and read-only vs edit scope; keep edits disjoint.

### Codex background tasks

When Zach explicitly asks for background/new tasks (including an explicit `$delegate`/overnight fan-out), use the task/thread tools. Choose:

- saved project or projectless target;
- local checkout or isolated worktree;
- exact model name as currently listed;
- exact supported reasoning effort.

Record the returned task ID. Follow-ups can keep or override model/effort. Use task-reading/steering tools to monitor; do not make Zach open the task manually.

When Zach explicitly asks for real additional ChatGPT/Codex sessions, create the tasks rather than returning prompt text. A queued client/worktree identifier is not a running task: wait for the concrete thread and worktree, record both, and relaunch safely if setup never materializes.

### Exact Codex CLI worker

For a self-contained noninteractive worker when exact routing matters:

```powershell
codex exec -C "C:\absolute\folder" -m gpt-5.6-terra -c 'model_reasoning_effort="high"' "<self-contained task>"
```

Use read-only sandbox for research and an isolated worktree for edits. Headless workers do not have live computer use.

### Cursor

The reliable Windows path is currently the Cursor GUI; do not assume `cursor-agent` exists. Open the exact folder (`cursor -n <folder>`), use live computer control to confirm the folder, choose the verified current model and effort/mode, paste the task, and monitor permission prompts/output. Cursor already has broad routine execution permissions; compensate with worktree isolation, no-secret/no-push/no-deploy constraints, and your own diff review.

Headless Cursor remains unavailable until the runner can prove exact Cursor model and effort routing; executable discovery alone is not sufficient. Use the GUI path or another worker. If headless support is explicitly verified later, copy the current invocation from `offload.py --help` and supply every required routing field: caller, different target, mode, exact model, exact effort, and an absolute existing folder, plus any applicable sandbox or permission acknowledgement.

When Zach explicitly asks for a real Cursor session, open the exact isolated folder, visibly confirm the current model/mode, stage the bounded packet, satisfy the required external-message confirmation, submit it, and monitor the actual run. Do not substitute a saved prompt for a launched worker.

### Claude

Within this run it is a monitored lane like any other: it does not become the master context holder or automatic final gate for work you own. Use an isolated folder and independently verify everything it returns. (Opened directly by Zach, Claude is a full orchestrator in its own right.)

Verify desktop and CLI authentication separately; one may be signed in while the other is not. When Zach explicitly asks for a real Claude session, choose the authenticated surface, select the exact folder/model/effort, stage the bounded packet, satisfy the required external-message or OAuth confirmation, submit it, and monitor it to a terminal report. Do not claim a staged prompt or a logged-out CLI is a running worker.

### Automations

Use a standalone automation only for recurring or scheduled work. Pin model, reasoning effort, project, and local/worktree environment. Use a heartbeat when the request is specifically to continue the current task soon. Never substitute an automation for monitoring a worker already in flight.

## 5. Write complete worker packets

Every packet includes:

1. exact outcome and why it matters;
2. exact model, effort/mode, folder/worktree, and branch;
3. files/URLs/state to read first;
4. complete relevant decisions and constraints;
5. scope exclusions and collision boundaries;
6. acceptance criteria and verification commands/runtime checks;
7. evidence format required at completion;
8. sensitive-action prohibitions;
9. instruction to report blockers with evidence and propose alternatives;
10. instruction to stop after its lane rather than invent adjacent work.

Do not leak the intended answer into an independent review prompt. Reviewers should receive the artifact, requirements, and rubric, not the root agent's diagnosis.

## 6. Create the durable goal

For three or more lanes or work expected to exceed one hour, create a Codex goal automatically. State the end condition, not the activity. Keep it active until every required lane is terminal and integrated; a goal is not a pause mechanism.

## 7. Dispatch early and monitor actively

Start all independent lanes as soon as their packets are complete. Maintain an outstanding-work ledger:

| ID | Worker/task ID | Model/effort | Folder | State | Last evidence | Next check/trigger |
|---|---|---|---|---|---|---|

While workers run:

- continue useful root work;
- inspect progress at intervals matched to expected duration;
- read actual outputs/diffs, not status labels alone;
- if output is empty, truncated, auth-limited, permission-blocked, or off-scope, treat it as non-terminal;
- send specific corrective feedback and require another pass;
- recover interrupted lanes from their task/thread/process ID and artifacts;
- terminate or clean up finished/failed helpers and dev servers.

Never write the final Read-Me while anything dispatched this turn is running, queued without a trigger, or awaiting unreviewed integration.

## 8. Integrate through a quality loop

For every lane:

1. Inspect the artifact/diff and compare it with the original acceptance criteria.
2. Run relevant typecheck/tests/build/data checks.
3. Score correctness, completeness, resilience, UX/data truthfulness, and evidence.
4. Run an adversarial/independent review for high-risk work.
5. Feed failures back to the responsible lane or fix them at root.
6. Re-run affected gates.
7. For user-facing work, invoke `$codexaudit` and use the actual app; test the changed path plus adjacent obvious failures.
8. Mark verified only with concrete evidence.

Quality is iterative. A worker running for hours, a clean exit code, a commit, or a green build is not sufficient by itself.

## 9. Reconcile and close

Before finishing:

- compare the original message line-by-line with the obligation ledger;
- ensure every item is verified, waiting on a named external condition with a trigger, obsolete/rejected with reason, or actively owned on the board;
- update model/effort/folder and evidence for each handoff;
- update durable decisions/memory without confusing proposals with Zach's decisions;
- close the goal only after the objective is actually achieved.

The final Read-Me reports outcomes and remaining genuine blockers. It never says "done" while an item is merely dispatched, remembered, or unverified.
