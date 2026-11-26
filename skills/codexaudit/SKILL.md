---
name: codexaudit
description: Autonomous live computer-use audit, remediation, and re-audit loop for a running app or visible workflow. Invoke explicitly as $codexaudit with an optional focus, and invoke automatically after substantive user-facing changes or during overnight verification. The orchestrating session launches and uses the real app like a skeptical user, records evidence, converts failures into tasks, fixes authorized defects, reruns automated gates, and repeats the live audit until acceptance criteria pass. It does not require Zach to paste a prompt into another session or report "done."
---

# Codex Audit

Use the actual product. A build or test result is only one gate; user-facing work is not verified until the running experience has been exercised.

## 1. Establish scope and authority

Infer:

- app/repo and exact absolute folder;
- live deployment, local web URL, desktop executable, or launch command;
- newest changed flows (audit these first);
- adjacent flows likely affected;
- user roles/data needed;
- destructive or sensitive actions that must not be exercised.

Default to a full-app sweep when no focus is supplied. A focused audit still includes a quick general pass for blank screens, literal `undefined`/`NaN`, dead navigation, console/runtime errors, and obviously broken layout or data.

Use a deep-tier model at high/max effort when taste, product judgment, or ambiguous failures matter. A separate independent audit task may use a balanced-tier model at high effort in the exact repo folder; state model, effort, and folder in the task itself. Do not use a separate task merely to avoid using the computer directly.

## 2. Write the audit matrix

Turn requirements and recent changes into concrete actions and expected observations:

| ID | Exact path/action | Expected result | Risk | Evidence |
|---|---|---|---|---|

Include as relevant:

- launch, sign-in visibility, navigation, primary happy paths;
- loading, empty, error, retry, offline/degraded, and stale-data behavior;
- realistic user inputs and boundary values;
- buttons, links, keyboard actions, back navigation, and persistence;
- copy, numbers, date/ticker/entity consistency, and truthfulness versus current reality;
- responsive/mobile widths, clipping, safe areas, motion, focus, and readability;
- adjacent surfaces sharing state, components, APIs, or routing;
- performance symptoms visible to a user.

Do not exercise purchases, trades, destructive data changes, account/security changes, credential entry, private messages, or external sends without explicit confirmation. Use reversible test data only.

## 3. Launch and operate

Use live Windows computer control. Prefer Microsoft Edge for visible browser QA unless the app requires another surface.

1. Start the app using its proven project workflow.
2. Confirm the visible build/deployment is the intended one.
3. Execute every audit-matrix action, not a representative subset.
4. Record PASS/FAIL, exactly what appeared, and screenshots/log references when useful.
5. Note unexpected issues even if outside the initial focus; Zach's examples are representative, not exhaustive.

For external data, spot-check against current authoritative sources. Never judge market/current facts from memory.

## 4. Preserve evidence

Use an existing repo QA convention when present. Otherwise write:

- findings: `docs/qa/codex-<focus>-qa-<YYYY-MM-DD>.md`;
- screenshots: `docs/qa/screenshots/`.

Each finding contains severity, reproducible steps, expected vs observed, evidence, likely scope/class, and acceptance criteria for the fix. Add every confirmed failure to the current task plan/obligation ledger; a findings doc alone is not remediation.

For a read-only audit request, stop after evidence and triage. For normal build/overnight work, continue automatically into repair.

## 5. Triage and repair

Classify findings:

- **Confirmed defect:** fix within the authorized project scope.
- **Whole-class defect:** inspect and fix adjacent instances, not just the screenshot example.
- **Taste/product fork:** recommend a direction; ask only when Zach retained the decision.
- **External/data/service issue:** verify the external cause and implement the best graceful behavior possible.
- **Not reproducible:** rerun with captured state; do not dismiss it from one failed reproduction.

After code changes:

1. run the repo's relevant static checks/tests/build;
2. inspect the diff for unintended changes;
3. reopen/reload the real app;
4. retest the original failure and adjacent cases;
5. update the finding to PASS only with observed evidence.

## 6. Repeat until terminal

Run audit -> repair -> automated verification -> live re-audit until:

- all acceptance criteria pass;
- remaining items require a named sensitive action/Zach decision/external state and have an owner + trigger on the active board; or
- the app cannot be run after exhausting safe in-scope recovery paths, with concrete blocker evidence.

Do not call the work done because the first audit found few issues, the fix compiled, or a worker said it was complete. The final quality gate belongs to the Codex orchestrator.

## 7. Close

Report the final pass/fail count, fixes made, automated gates, live behaviors observed, and genuine unresolved blockers. Keep the QA evidence with the change when the repo expects it. Reconcile every audit finding against `~/workspace/ORCHESTRATION-BOARD.md` before the final Read-Me.
