#!/usr/bin/env python3
"""Restore operating-config surfaces from this repo back onto the machine.

This is the reverse of ``snapshot.py`` and the reason the repo exists: after a bad
edit, a tool reinstall, or a move to a new machine, this puts the operating rules,
hooks, briefs, and skills back where the tools actually read them.

It is deliberately cautious, because it overwrites live config:

* Dry run by default. You must pass ``--apply`` to write anything.
* Every file it would overwrite is backed up to ``<file>.pre-restore-<stamp>`` first.
* It restores only what the snapshot manifest covers, and never touches secrets.

Usage
-----
    python restore.py                    # show what would change (safe)
    python restore.py --apply            # actually restore, with backups
    python restore.py --apply --only claude   # restore one surface group
"""

import argparse
import filecmp
import os
import shutil
import sys
import time

REPO = os.path.dirname(os.path.abspath(__file__))
DEST_ROOT = os.path.join(REPO, "surfaces")

sys.path.insert(0, REPO)
from snapshot import MANIFEST, forbidden  # noqa: E402

GROUPS = ("operating-agreement", "claude", "codex", "cursor", "skills",
          "board", "account-switch")


def iter_pairs(only=None):
    """Yield (snapshot_path, live_path) for every file the snapshot holds."""
    for src, rel_dst, kind in MANIFEST:
        group = rel_dst.split("/")[0]
        if only and group != only:
            continue
        snap = os.path.join(DEST_ROOT, rel_dst.replace("/", os.sep))
        if kind == "tree":
            if not os.path.isdir(snap):
                continue
            for root, dirs, files in os.walk(snap):
                dirs[:] = [d for d in dirs if d != ".git"]
                for name in files:
                    s = os.path.join(root, name)
                    rel = os.path.relpath(s, snap)
                    yield s, os.path.join(src, rel)
        else:
            if os.path.exists(snap):
                yield snap, src


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="actually write files (default is a dry run)")
    ap.add_argument("--only", choices=GROUPS,
                    help="restore only one surface group")
    args = ap.parse_args()

    stamp = time.strftime("%Y%m%d-%H%M%S")
    identical = same = 0
    planned = []

    for snap, live in iter_pairs(args.only):
        if forbidden(live):
            continue
        if os.path.exists(live) and filecmp.cmp(snap, live, shallow=False):
            identical += 1
            continue
        planned.append((snap, live, "overwrite" if os.path.exists(live) else "create"))

    print(f"Restore plan{' for ' + args.only if args.only else ''}")
    print("=" * 44)
    print(f"  {identical} files already identical")
    if not planned:
        print("  Nothing to restore - the machine matches the snapshot.")
        return 0

    for snap, live, action in planned:
        print(f"  {action:<9} {live}")

    if not args.apply:
        print(f"\n{len(planned)} file(s) would change. This was a DRY RUN.")
        print("Rerun with --apply to write them (originals are backed up first).")
        return 0

    written = 0
    for snap, live, action in planned:
        os.makedirs(os.path.dirname(live), exist_ok=True)
        if os.path.exists(live):
            shutil.copy2(live, f"{live}.pre-restore-{stamp}")
        shutil.copy2(snap, live)
        written += 1

    print(f"\nRestored {written} file(s).")
    print(f"Originals saved alongside as *.pre-restore-{stamp}")
    print("Now re-run the hooks once to confirm they still emit "
          "(see README.md 'Verifying a restore').")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
