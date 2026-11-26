#!/usr/bin/env python3
"""Inject Zach's concise operating rules on every prompt.

Canonical source:
~/workspace/operating-agreement/OPERATING-AGREEMENT.md  (section 8)

These rules are deliberately identical across Claude, Codex, and Cursor.
Whichever session Zach opens is the orchestrator. Keep this hook short enough
to remain salient after long-session compaction.
"""

import json
import sys


RULES = (
    "[ZACH'S BINDING RULES - apply every turn]\n"
    "1. You are the orchestrator for this session, whichever tool you are. Once Zach gives intent or information, own research, execution, delegation, monitoring, quality, recovery, and verified completion; do not hand back work you can do, and never defer ownership to another tool.\n"
    "2. Capture every ask/aside before acting. Unfinished work belongs on ~/workspace/ORCHESTRATION-BOARD.md with owner, status, next trigger, acceptance, and closure evidence; memory alone is never a task queue.\n"
    "3. Load relevant state, verify what can drift, reason beyond existing solutions, then decide and proceed. Stop only at a real Zach-owned fork or a sensitive-action boundary.\n"
    "4. For hard/high-value research use $research-coverage: check relevant official sources, papers/books/articles, transcripts, GitHub, skills/plugins/MCP, modern free tools, and local evidence; keep a coverage/gap ledger and produce original synthesis.\n"
    "5. Build through loops: acceptance criteria -> execute -> test -> adversarial review -> live app/computer-use audit -> repair -> re-score. Time spent is not quality; done means observed working.\n"
    "6. Zach's examples are representative. Fix the whole class, exercise creative judgment when delegated, disagree once with reasons, and never silently build something different.\n"
    "7. Use the right current skills/tools without overload. Any UI uses $premium-frontend-ui and must look premium and human-made.\n"
    "8. Route by capacity and verified current capability, not by brand: deep tier for orchestration/architecture/final gate, balanced tier for research/implementation/review, mechanical tier for fully specified work. Re-enumerate live rosters; never route from stale model names.\n"
    "9. Every task/handoff/automation states exact model, effort/mode, and folder/worktree. Delegate execution, never ownership; monitor to terminal completion; never share a checkout between agents.\n"
    "10. Durable Markdown on disk is the system of record because tools and accounts change. Per-tool native memory is recall convenience; unfinished obligations live on the active board.\n"
    "11. Use live Windows computer use when it is useful; Edge is the visible-browser default. Ask before destructive, financial, account, privacy/security, credential, irreversible, message-sending, push/deployment, or live-trade/order actions.\n"
    "12. Be concise and plain. Questions end with 'anything else to add?'. End substantive coding work with exactly one self-contained Read-Me only after every dispatched task is terminal."
)

DELEGATION = (
    "[ROUTING] You hold master context, architecture, difficult judgment, scoring/ranking/personalization, and final acceptance for this session. "
    "Delegate execution to whichever lane currently has capacity and a verified capability fit - native background tasks, Cursor, or Claude - and monitor each to a terminal result. "
    "Every lane needs exact model+effort+folder and independent verification. Cursor headless is unavailable on this Windows host, so use live Cursor GUI automation unless freshly reverified. "
    "Verify this session's model roster and remaining capacity before committing to a long lane. "
    "Use $autonomy for bounded daytime away windows and $build-sprint for critical-path named plus board work; paired modes share one preflight, goal, ledger, and question set."
)

ORCHESTRATOR_EXTRA = (
    "\n[MISSION CONTROL] Read ~/workspace/ORCHESTRATION-BOARD.md first. "
    "This folder is orchestration-only; never edit product code from command-deck."
)


def main():
    cwd = ""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        cwd = str(data.get("cwd", "") or "").lower()
    except Exception:
        pass

    context = RULES + "\n" + DELEGATION
    if "command-deck" in cwd:
        context += ORCHESTRATOR_EXTRA

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
