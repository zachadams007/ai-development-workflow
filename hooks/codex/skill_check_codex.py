#!/usr/bin/env python3
"""Remind Codex to use the smallest high-value set of current skills."""

import json
import sys


VISUAL_TERMS = (
    "ui", "frontend", "front-end", "design", "css", "tailwind", "motion",
    "three.js", "threejs", "r3f", "webgl", "webgpu", "shader", "gltf",
)
RESEARCH_TERMS = (
    "research", "landscape", "latest", "current tools", "every article",
    "papers", "books", "youtube", "transcript", "github repos", "comprehensive",
)
DELEGATE_TERMS = (
    "delegate", "parallel", "background sessions", "multiple tasks", "overnight",
)
AUDIT_TERMS = (
    "audit the app", "click through", "use the app", "computer use", "qa the app",
)

BASE = (
    "[SKILL CHECK] Before acting, scan available skills and invoke the smallest set that materially improves this task. "
    "Verify current tools/skills live when they may have changed; do not overload the context or route taste/final judgment away from Codex by default."
)


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    prompt = str(data.get("prompt", "") or "").lower()
    additions = []
    if any(term in prompt for term in VISUAL_TERMS):
        additions.append("UI/visual: use $premium-frontend-ui; keep product taste and final visual acceptance on Codex/Sol unless a verified specialist is better.")
    if any(term in prompt for term in RESEARCH_TERMS):
        additions.append("Deep/current research: use $research-coverage and keep a source-family gap ledger.")
    if any(term in prompt for term in DELEGATE_TERMS):
        additions.append("Multi-lane work: use $delegate; $overnight must invoke it after plan confirmation.")
    if any(term in prompt for term in AUDIT_TERMS):
        additions.append("Running-app verification: use $codexaudit directly; do not hand Zach a shuttle prompt.")
    context = BASE
    if additions:
        context += "\n- " + "\n- ".join(additions)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
