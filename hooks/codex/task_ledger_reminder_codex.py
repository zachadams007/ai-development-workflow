#!/usr/bin/env python3
"""Prevent multi-ask messages and deferred obligations from disappearing."""

import json
import re
import sys


BASE = (
    "[OBLIGATION CAPTURE] If this message contains 2+ asks, asides, future items, constraints, or questions, enumerate every one before acting. "
    "Before ending, each item must be verified complete or recorded in ~/workspace/ORCHESTRATION-BOARD.md with ID, source, owner/lane, status, exact model+effort+folder when delegated, next trigger/action, acceptance criteria, and closure evidence. "
    "'Saved to memory', 'prompt supplied', 'dispatched', or 'build passed' are not completion. Reconcile the original message line-by-line."
)

DETAIL = (
    "\n[BRAIN-DUMP DETECTED] Create/update the explicit obligation ledger first. Small side notes count equally; use $delegate for independent lanes and keep monitoring until every lane is terminal."
)

LIST_RE = re.compile(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\S")


def looks_multi(prompt):
    if len(prompt) > 500 or prompt.count("\n\n") >= 2:
        return True
    if len(LIST_RE.findall(prompt)) >= 2:
        return True
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", prompt) if len(s.strip()) > 20]
    return len(sentences) >= 5


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    prompt = str(data.get("prompt", "") or "")
    context = BASE + (DETAIL if looks_multi(prompt) else "")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
