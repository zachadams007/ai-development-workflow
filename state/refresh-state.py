#!/usr/bin/env python3
"""Regenerate the LIVE STATE block inside START-HERE.md.

START-HERE.md is the standing front door: any session, in any tool, can be pointed at
it and immediately know how things work, what exists, and where every project stands.
The narrative half is hand-written and stable. The factual half - accounts, skills,
MCP servers, project git state, memory counts, open board items - goes stale within
days, so it is generated here instead of typed.

Everything is read live off the disk at run time. Nothing is cached, and every probe is
individually guarded so one missing folder cannot blank the whole document.

Usage
-----
    python state/refresh-state.py          # rewrite the block in START-HERE.md
    python state/refresh-state.py --stdout   # print the block, change nothing
"""

import argparse
import io
import json
import os
import re
import subprocess
import time

HOME = os.path.expanduser("~")
DESKTOP = os.path.join(HOME, "Desktop")
DECK = os.path.join(DESKTOP, "command-deck")
TARGET = os.path.join(DECK, "START-HERE.md")
BOARD = os.path.join(DESKTOP, "ORCHESTRATION-BOARD.md")

BEGIN = "<!-- LIVE-STATE:BEGIN -->"
END = "<!-- LIVE-STATE:END -->"

# Desktop folders that are real projects, in priority order.
PROJECTS = [
    ("Catalyzed Alpha", "catalyzed-alpha"),
    ("Praxis", "praxis"),
    ("trading-bot", "trading-bot"),
    ("3D print site", "3d-print-site-github"),
    ("command-deck", "command-deck"),
    ("operating-config", "operating-config"),
]


def safe(fn, default="unknown"):
    try:
        result = fn()
        return default if result is None else result
    except Exception as exc:  # noqa: BLE001 - a probe failing must never break the doc
        return f"{default} ({type(exc).__name__})"


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, timeout=30)
    return proc.stdout.strip() if proc.returncode == 0 else None


def read_json(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- probes

def probe_account():
    d = read_json(os.path.join(HOME, ".claude.json"))
    oa = d.get("oauthAccount", {}) or {}
    return {
        "email": oa.get("emailAddress", "unknown"),
        "org": oa.get("organizationName") or oa.get("organizationType", "unknown"),
        "tier": oa.get("organizationRateLimitTier") or oa.get("seatTier", "unknown"),
        "billing": oa.get("billingType", "unknown"),
        "mcp": sorted((d.get("mcpServers") or {}).keys()),
    }


def probe_settings():
    d = read_json(os.path.join(HOME, ".claude", "settings.json"))
    return {
        "model": d.get("model", "unset"),
        "plugins": sorted((d.get("enabledPlugins") or {}).keys()),
        "hooks": sorted((d.get("hooks") or {}).keys()),
        "workflows": d.get("enableWorkflows", False),
    }


def probe_skills():
    out = {}
    for label, path in (("shared (~/.agents/skills)", os.path.join(HOME, ".agents", "skills")),
                        ("claude (~/.claude/skills)", os.path.join(HOME, ".claude", "skills"))):
        if not os.path.isdir(path):
            out[label] = []
            continue
        out[label] = sorted(
            n for n in os.listdir(path)
            if os.path.isfile(os.path.join(path, n, "SKILL.md"))
        )
    return out


def probe_hooks_live():
    """A hook that throws stops injecting rules silently. Prove each one still emits."""
    checks = [
        ("claude/preference_enforcer", os.path.join(HOME, ".claude", "hooks", "preference_enforcer.py")),
        ("claude/task_ledger_reminder", os.path.join(HOME, ".claude", "hooks", "task_ledger_reminder.py")),
        ("codex/preference_enforcer_codex", os.path.join(HOME, ".codex", "hooks", "preference_enforcer_codex.py")),
        ("codex/task_ledger_reminder_codex", os.path.join(HOME, ".codex", "hooks", "task_ledger_reminder_codex.py")),
    ]
    results = []
    for name, path in checks:
        if not os.path.exists(path):
            results.append((name, "MISSING"))
            continue
        try:
            proc = subprocess.run(["python", path], input='{"prompt":"x","cwd":"y"}',
                                  capture_output=True, text=True, timeout=30)
            ok = proc.returncode == 0 and len(proc.stdout.strip()) > 50
            results.append((name, "ok" if ok else f"FAILING (rc={proc.returncode})"))
        except Exception as exc:  # noqa: BLE001
            results.append((name, f"FAILING ({type(exc).__name__})"))
    return results


def probe_project(folder):
    path = os.path.join(DESKTOP, folder)
    info = {"path": path, "exists": os.path.isdir(path)}
    if not info["exists"]:
        return info
    if os.path.isdir(os.path.join(path, ".git")):
        info["branch"] = git(path, "rev-parse", "--abbrev-ref", "HEAD") or "?"
        info["last"] = git(path, "log", "-1", "--format=%h %ad %s", "--date=short") or "?"
        dirty = git(path, "status", "--porcelain")
        info["dirty"] = len(dirty.splitlines()) if dirty else 0
        ahead = git(path, "rev-list", "--count", "@{u}..HEAD")
        info["unpushed"] = ahead if ahead is not None else "no upstream"
    # project memory lives under a mangled path key
    key = "C--Users-dev-Desktop-" + folder.replace(" ", "-").replace("(", "").replace(")", "")
    memdir = os.path.join(HOME, ".claude", "projects", key, "memory")
    if os.path.isdir(memdir):
        info["memory"] = len([f for f in os.listdir(memdir) if f.endswith(".md")])
        info["memory_path"] = memdir
    return info


def probe_memory():
    root = os.path.join(HOME, ".claude", "projects")
    rows = []
    if os.path.isdir(root):
        for name in os.listdir(root):
            memdir = os.path.join(root, name, "memory")
            if os.path.isdir(memdir):
                n = len([f for f in os.listdir(memdir) if f.endswith(".md")])
                if n:
                    short = name.replace("C--Users-dev-Desktop-", "").replace("C--Users-dev", "(home)")
                    rows.append((short, n))
    rows.sort(key=lambda r: -r[1])
    intent = os.path.join(HOME, ".claude", "memory", "intent")
    n_intent = 0
    if os.path.isdir(intent):
        for _, _, files in os.walk(intent):
            n_intent += len([f for f in files if f.endswith(".md")])
    return rows, n_intent


def probe_board():
    """Pull the open obligation IDs out of the board so status is visible here."""
    if not os.path.exists(BOARD):
        return []
    with io.open(BOARD, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    items = []
    for m in re.finditer(r"^###\s+([A-Z]+-\d+)\s+-+\s+(.+?)\s*$", text, re.M):
        ident, title = m.group(1), m.group(2)
        tail = text[m.end():m.end() + 400]
        state = "OPEN"
        for flag in ("DONE", "COMPLETE", "WAITING", "QUEUED", "IN PROGRESS", "OPEN"):
            if flag in title.upper() or flag in tail.upper()[:200]:
                state = flag
                break
        items.append((ident, re.sub(r"\s*\((DONE|OPEN|WAITING|QUEUED)[^)]*\)", "", title).strip(), state))
    return items


# --------------------------------------------------------------------------- render

def render():
    L = []
    add = L.append
    stamp = time.strftime("%Y-%m-%d %H:%M")

    add(BEGIN)
    add("")
    add(f"*Everything below is generated from the live machine. Last refreshed: "
        f"**{stamp}**. Regenerate with `python src/refresh-state.py` — if this "
        f"timestamp looks old, run it before trusting the numbers.*")
    add("")

    # -- account / tools
    acct = safe(probe_account, {})
    sett = safe(probe_settings, {})
    add("### Signed-in account and tools")
    add("")
    if isinstance(acct, dict) and acct:
        add(f"- **Claude account:** `{acct.get('email')}` — org `{acct.get('org')}`, "
            f"rate-limit tier `{acct.get('tier')}`, billing `{acct.get('billing')}`")
    else:
        add(f"- **Claude account:** could not read (`{acct}`)")
    if isinstance(sett, dict) and sett:
        add(f"- **Default model:** `{sett.get('model')}` · workflows enabled: "
            f"`{sett.get('workflows')}`")
        add(f"- **Plugins:** {', '.join(f'`{p}`' for p in sett.get('plugins', [])) or 'none'}")
        add(f"- **Hook events:** {', '.join(f'`{h}`' for h in sett.get('hooks', [])) or 'none'}")
    if isinstance(acct, dict) and acct.get("mcp"):
        add(f"- **Local MCP servers:** {', '.join(f'`{m}`' for m in acct['mcp'])}")
    add("- **Codex:** config at `~/.codex`. "
        "Verify access before routing work there.")
    add("- **Cursor:** active, GUI automation only (headless `cursor-agent` absent).")
    add("")

    # -- rule enforcement actually working
    add("### Rule enforcement (are the binding rules actually firing?)")
    add("")
    hooks = safe(probe_hooks_live, [])
    if isinstance(hooks, list) and hooks:
        for name, status in hooks:
            mark = "OK  " if status == "ok" else "FAIL"
            add(f"- `{mark}` {name} — {status}")
        if any(s != "ok" for _, s in hooks):
            add("")
            add("  > A failing hook means rules stop being injected **silently**. "
                "Restore from `Desktop/operating-config` (`python restore.py --apply`).")
    add("")

    # -- projects
    add("### Projects — where each one actually stands")
    add("")
    add("| Project | Branch | Last commit | Uncommitted | Unpushed | Memory |")
    add("|---|---|---|---|---|---|")
    for label, folder in PROJECTS:
        p = safe(lambda f=folder: probe_project(f), {})
        if not isinstance(p, dict) or not p.get("exists"):
            add(f"| {label} | — | *folder not found* | — | — | — |")
            continue
        branch = p.get("branch", "not a repo")
        last = p.get("last", "—")
        dirty = p.get("dirty")
        dirty_s = "clean" if dirty == 0 else (f"**{dirty} files**" if dirty else "—")
        unpushed = p.get("unpushed", "—")
        unpushed_s = ("clean" if str(unpushed) == "0" else f"**{unpushed}**")
        mem = p.get("memory")
        mem_s = f"{mem} notes" if mem else "—"
        add(f"| {label} | `{branch}` | {last} | {dirty_s} | {unpushed_s} | {mem_s} |")
    add("")
    add("Open a project's `memory/MEMORY.md` for its decision history before doing "
        "feature work there.")
    add("")

    # -- skills
    add("### Workflows and skills available right now")
    add("")
    skills = safe(probe_skills, {})
    if isinstance(skills, dict):
        for label, names in skills.items():
            core = [n for n in names if not n.startswith(("threejs-", "webgpu-", "cockpit"))]
            extra = len(names) - len(core)
            add(f"**{label}** — {len(names)} total")
            add("")
            add("  " + ", ".join(f"`{n}`" for n in core) +
                (f" · plus {extra} threejs/webgpu/cockpit specialists" if extra else ""))
            add("")
    add("Plugin skills (ecc, compound-engineering) add many more; they are listed in "
        "each session's skill roster rather than duplicated here.")
    add("")

    # -- memory map
    add("### Memory map")
    add("")
    rows, n_intent = safe(probe_memory, ([], 0))
    if rows:
        top = rows[:8]
        add("Per-project notes under `~/.claude/projects/<key>/memory/`:")
        add("")
        add("  " + " · ".join(f"**{name}** {n}" for name, n in top))
        if len(rows) > 8:
            add("")
            add(f"  …plus {len(rows) - 8} smaller project folders.")
        add("")
    add(f"Intent ledger (`~/.claude/memory/intent/`): **{n_intent}** files, spans every project.")
    add("")
    add("Trust order: **durable Markdown on disk** > the active board > per-tool native "
        "memory > archives. Tools and accounts change; the disk does not.")
    add("")

    # -- board
    add("### Open obligations")
    add("")
    items = safe(probe_board, [])
    if isinstance(items, list) and items:
        shown = [i for i in items if i[2] not in ("DONE", "COMPLETE")][:12]
        if shown:
            for ident, title, state in shown:
                add(f"- **{ident}** ({state}) — {title}")
        else:
            add("- No open items parsed from the board.")
        add("")
        add(f"Parsed {len(items)} structured items from the board. The board itself is "
            f"the authority: `{BOARD}`")
    else:
        add(f"Could not parse board items. Read it directly: `{BOARD}`")
    add("")

    # -- backups
    add("### Backups")
    add("")
    for label, folder, remote in (
        ("command-deck", "command-deck", "github.com/owner/command-deck"),
        ("operating-config", "operating-config", "github.com/owner/operating-config"),
    ):
        path = os.path.join(DESKTOP, folder)
        last = safe(lambda p=path: git(p, "log", "-1", "--format=%h %ad", "--date=short"), "?")
        add(f"- **{label}** → `{remote}` · last commit {last}")
    add("- Product repos (`catalyzed-alpha`, `praxis`, `trading-bot`) back up to their "
        "own private repos under the same account.")
    add("")
    add(END)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stdout", action="store_true", help="print the block instead of writing")
    args = ap.parse_args()

    block = render()
    if args.stdout:
        print(block)
        return 0

    if not os.path.exists(TARGET):
        raise SystemExit(f"START-HERE.md not found at {TARGET}")
    with io.open(TARGET, encoding="utf-8") as fh:
        doc = fh.read()
    if BEGIN not in doc or END not in doc:
        raise SystemExit("START-HERE.md is missing the LIVE-STATE markers.")

    start = doc.index(BEGIN)
    end = doc.index(END) + len(END)
    with io.open(TARGET, "w", encoding="utf-8") as fh:
        fh.write(doc[:start] + block + doc[end:])
    print(f"Refreshed live state in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
