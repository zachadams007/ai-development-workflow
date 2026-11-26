#!/usr/bin/env python3
"""Keep this session's obligations synchronized with the shared active board."""

import json
import re
import sys


BASE = (
    "[OBLIGATION CAPTURE] If this message contains 2+ asks/asides/future items, enumerate all of them before acting. "
    "Before ending, each is verified complete or recorded in ~/workspace/ORCHESTRATION-BOARD.md with source, owner/lane, status, model+effort+folder, next trigger, acceptance, and evidence. "
    "'Saved to memory', 'prompt supplied', 'dispatched', or 'build passed' are not completion. You own integration and final closure for this session; reconcile the original message line-by-line."
)

DETAIL = "\n[BRAIN-DUMP DETECTED] Capture the full ledger first; small side notes count equally. Use delegate for independent lanes and keep monitoring until every lane is terminal."
LIST_RE = re.compile(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\S")


def looks_multi(prompt):
    if len(prompt) > 500 or prompt.count("\n\n") >= 2 or len(LIST_RE.findall(prompt)) >= 2:
        return True
    return len([s for s in re.split(r"(?<=[.!?])\s+", prompt) if len(s.strip()) > 20]) >= 5


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    prompt = str(data.get("prompt", "") or "")
    print(BASE + (DETAIL if looks_multi(prompt) else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
