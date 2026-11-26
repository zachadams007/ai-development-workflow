#!/usr/bin/env python3
"""Snapshot Zach's scattered operating-config surfaces into this repo, then commit.

Why this exists
---------------
The highest-authority files in the setup (the canonical operating agreement, the
every-turn hooks, the per-tool briefs, the skills) live in unversioned home-config
directories. A tool change, an account switch, or a bad edit could lose them with no
history to recover from. This repo gives them one git history.

Design rules
------------
* **Explicit allowlist only.** Never sweep a directory blindly - a sweep of
  ``~/.claude`` would pull in ``secrets/``, ``.credentials.json``, and key files.
* **Secret scan before commit.** If anything that looks like a live credential lands
  in the snapshot, abort loudly rather than committing it.
* **Copy, not symlink.** Windows symlinks need admin or developer mode and break
  under some tooling. A copy always works.
* **Read-only toward the sources.** This script never writes outside this repo.
  Going the other direction is ``restore.py``.

Usage
-----
    python snapshot.py              # copy surfaces in, report, commit if changed
    python snapshot.py --no-commit  # copy and report only
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")
DESKTOP = os.path.join(HOME, "Desktop")
REPO = os.path.dirname(os.path.abspath(__file__))
DEST_ROOT = os.path.join(REPO, "surfaces")

# (source path, destination path inside surfaces/, kind)
#   kind "file" copies one file; kind "glob" copies matching files in one directory;
#   kind "tree" copies a directory subtree filtered by extension.
MANIFEST = [
    # --- canonical ---
    (os.path.join(DESKTOP, "operating-agreement", "OPERATING-AGREEMENT.md"),
     "operating-agreement/OPERATING-AGREEMENT.md", "file"),
    (os.path.join(DESKTOP, "operating-agreement", "CLAUDE.md"),
     "operating-agreement/CLAUDE.md", "file"),
    (os.path.join(DESKTOP, "operating-agreement", "AGENTS.md"),
     "operating-agreement/AGENTS.md", "file"),
    (os.path.join(DESKTOP, "operating-agreement", "CONVERSATION-CONTEXT.md"),
     "operating-agreement/CONVERSATION-CONTEXT.md", "file"),

    # --- Claude control surfaces ---
    (os.path.join(HOME, ".claude", "CLAUDE.md"), "claude/CLAUDE.md", "file"),
    (os.path.join(HOME, ".claude", "settings.json"), "claude/settings.json", "file"),
    (os.path.join(HOME, ".claude", "hooks", "preference_enforcer.py"),
     "claude/hooks/preference_enforcer.py", "file"),
    (os.path.join(HOME, ".claude", "hooks", "task_ledger_reminder.py"),
     "claude/hooks/task_ledger_reminder.py", "file"),
    (os.path.join(HOME, ".claude", "hooks", "skill_check.py"),
     "claude/hooks/skill_check.py", "file"),
    (os.path.join(HOME, ".claude", "commands"), "claude/commands", "tree"),

    # --- Codex control surfaces ---
    (os.path.join(HOME, ".codex", "AGENTS.md"), "codex/AGENTS.md", "file"),
    (os.path.join(HOME, ".codex", "hooks", "preference_enforcer_codex.py"),
     "codex/hooks/preference_enforcer_codex.py", "file"),
    (os.path.join(HOME, ".codex", "hooks", "task_ledger_reminder_codex.py"),
     "codex/hooks/task_ledger_reminder_codex.py", "file"),
    (os.path.join(HOME, ".codex", "hooks", "skill_check_codex.py"),
     "codex/hooks/skill_check_codex.py", "file"),

    # --- Cursor control surfaces ---
    (os.path.join(HOME, ".cursor", "rules"), "cursor/rules", "tree"),

    # --- skills (authored workflow definitions) ---
    (os.path.join(HOME, ".agents", "skills"), "skills/agents", "tree"),
    (os.path.join(HOME, ".claude", "skills"), "skills/claude", "tree"),

    # --- operating docs ---
    (os.path.join(DESKTOP, "ORCHESTRATION-BOARD.md"), "board/ORCHESTRATION-BOARD.md", "file"),
]

TREE_EXTENSIONS = {".md", ".mdc", ".py", ".json", ".yaml", ".yml", ".txt", ".sh", ".ps1"}
SKIP_DIR_NAMES = {"__pycache__", ".git", "node_modules", "logs", ".venv"}

# Files that must NEVER be snapshotted, even if a manifest entry would reach them.
FORBIDDEN_SUBSTRINGS = (
    os.path.join(".claude", "secrets"),
    os.path.join(".claude", "keys"),
    ".credentials.json",
    "auth.json",
    ".gh-token",
    "secrets.txt",
    "api_key",
)

# Patterns that indicate a real credential slipped into a snapshotted file.
SECRET_PATTERNS = [
    (re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}"), "OpenAI-style API key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bey[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "JWT"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
]


def forbidden(path):
    low = path.lower().replace("/", os.sep)
    return any(bad.lower() in low for bad in FORBIDDEN_SUBSTRINGS)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_file(src, dst):
    """Copy src to dst. Returns 'new', 'changed', or 'same'."""
    if not os.path.exists(src):
        return "missing"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        if digest(src) == digest(dst):
            return "same"
        shutil.copy2(src, dst)
        return "changed"
    shutil.copy2(src, dst)
    return "new"


def copy_tree(src_dir, dst_dir):
    results = {"new": 0, "changed": 0, "same": 0, "skipped": 0}
    if not os.path.isdir(src_dir):
        return None
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
        for name in files:
            src = os.path.join(root, name)
            if forbidden(src):
                results["skipped"] += 1
                continue
            if os.path.splitext(name)[1].lower() not in TREE_EXTENSIONS:
                results["skipped"] += 1
                continue
            rel = os.path.relpath(src, src_dir)
            outcome = copy_file(src, os.path.join(dst_dir, rel))
            if outcome in results:
                results[outcome] += 1
    return results


def scan_for_secrets(root):
    findings = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
        for name in files:
            path = os.path.join(dirpath, name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append((os.path.relpath(path, root), label))
    return findings


def git(*args, check=True):
    proc = subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True)
    if check and proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise SystemExit(f"git {' '.join(args)} failed ({proc.returncode})")
    return proc.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-commit", action="store_true",
                    help="copy and report, but do not create a commit")
    args = ap.parse_args()

    print("Snapshotting operating-config surfaces\n" + "=" * 44)
    missing = []
    totals = {"new": 0, "changed": 0, "same": 0, "missing": 0}

    for src, rel_dst, kind in MANIFEST:
        dst = os.path.join(DEST_ROOT, rel_dst.replace("/", os.sep))
        if forbidden(src):
            print(f"  REFUSED (forbidden path)  {src}")
            continue
        if kind == "tree":
            res = copy_tree(src, dst)
            if res is None:
                print(f"  MISSING  {rel_dst}")
                missing.append(src)
                totals["missing"] += 1
            else:
                for k in ("new", "changed", "same"):
                    totals[k] += res[k]
                mark = "+" if (res["new"] or res["changed"]) else " "
                print(f"  {mark} tree  {rel_dst:<34} "
                      f"new={res['new']} changed={res['changed']} same={res['same']}")
        else:
            outcome = copy_file(src, dst)
            totals[outcome] = totals.get(outcome, 0) + 1
            if outcome == "missing":
                missing.append(src)
                print(f"  MISSING  {rel_dst}")
            else:
                mark = "+" if outcome in ("new", "changed") else " "
                print(f"  {mark} file  {rel_dst:<34} {outcome}")

    print("-" * 44)
    print(f"  new={totals['new']} changed={totals['changed']} "
          f"same={totals['same']} missing={totals['missing']}")

    print("\nScanning snapshot for credentials...")
    findings = scan_for_secrets(DEST_ROOT)
    if findings:
        print("  ABORT - possible secrets found in the snapshot:")
        for rel, label in findings:
            print(f"    {label}: surfaces/{rel}")
        print("\n  Nothing was committed. Remove the secret from the SOURCE file,")
        print("  delete the copy under surfaces/, and rerun.")
        return 2
    print("  clean")

    if missing:
        print("\nNote: these manifest entries do not exist on disk right now:")
        for m in missing:
            print(f"    {m}")
        print("  That is fine if the surface was intentionally retired -")
        print("  update MANIFEST in this script if it is gone for good.")

    if args.no_commit:
        print("\n--no-commit: stopping before commit.")
        return 0

    git("add", "-A")
    status = git("status", "--porcelain")
    if not status:
        print("\nNo changes to commit - snapshot already matches the live surfaces.")
        return 0

    changed_count = len(status.splitlines())
    git("commit", "-q", "-m",
        f"snapshot: operating-config surfaces ({changed_count} files)")
    print(f"\nCommitted {changed_count} changed files: {git('log', '-1', '--format=%h %s')}")
    print("Push is a separate, deliberate step - see README.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
