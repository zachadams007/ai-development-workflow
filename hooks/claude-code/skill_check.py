#!/usr/bin/env python3
"""Prompt Claude workers to use a small, relevant, current skill set."""

import json
import sys


VISUAL = ("ui", "frontend", "design", "css", "three.js", "threejs", "r3f", "webgl", "webgpu", "shader")
RESEARCH = ("research", "papers", "books", "transcript", "github repos", "comprehensive", "latest tools")


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    prompt = str(data.get("prompt", "") or "").lower()
    lines = [
        "[SKILL CHECK] Use the smallest set of available current skills that materially improves this bounded worker task; do not overload the context or install tools speculatively."
    ]
    if any(term in prompt for term in VISUAL):
        lines.append("Visual work: use premium-frontend-ui and relevant threejs skills; return the result to Codex for final taste/live-app acceptance.")
    if any(term in prompt for term in RESEARCH):
        lines.append("Deep/current research: use the shared research-coverage workflow and keep a source-family gap ledger.")
    print("\n- ".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
