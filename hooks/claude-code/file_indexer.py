#!/usr/bin/env python3
"""
Active memory file indexer for Claude sessions.

Scans Desktop / Downloads / Documents / Pictures for files modified in the
last 30 days and writes a structured index to ~/.claude/memory/files-index.md.

That file is pointed to by MEMORY.md, so every future Claude session inherits
a live view of what's on the device without any manual searching.

Run manually:  python file_indexer.py
Run quietly:   python file_indexer.py --quiet
Registered as: Windows Task Scheduler "ClaudeFileIndexer" (daily 9 AM)
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# ── scan targets ───────────────────────────────────────────────────────────────
HOME = Path.home()

SCAN_DIRS = [
    HOME / "Desktop",
    HOME / "Downloads",
    HOME / "Documents",
    HOME / "Pictures",
    HOME / "OneDrive" / "Desktop",      # common on Windows
    HOME / "OneDrive" / "Documents",
]

DAYS_BACK = 45   # wider window - beats "I made this last month"

# ── output locations ───────────────────────────────────────────────────────────
MEMORY_DIR = HOME / ".claude" / "memory"
OUT_MD     = MEMORY_DIR / "files-index.md"
OUT_JSON   = MEMORY_DIR / "files-index.json"

# ── classification ─────────────────────────────────────────────────────────────
IMAGE_EXT  = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif", ".bmp", ".tiff", ".svg", ".psd", ".ai"}
DOC_EXT    = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".rtf", ".md", ".pages", ".numbers", ".key"}
CODE_EXT   = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".swift", ".kt", ".java", ".html", ".css", ".scss", ".json", ".yaml", ".yml", ".toml", ".sh", ".ps1"}
VIDEO_EXT  = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
AUDIO_EXT  = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}

# Skip directory names anywhere in path
SKIP_DIR_NAMES = {
    ".git", "node_modules", "__pycache__", ".cache", ".venv", "venv",
    "Temp", "temp", ".tmp", "WindowsApps", "$RECYCLE.BIN",
    "System Volume Information", "ProgramData", ".claude",  # skip our own dir
    "dist", "build", ".next", "out",
    "target",          # Rust/Cargo build output
    ".fingerprint",    # Cargo incremental build metadata
    "deps",            # Rust deps artifacts (under target)
    ".gradle", ".mvn", # Java build dirs
}

# Skip by extension
SKIP_EXT = {".lnk", ".ini", ".dll", ".exe", ".sys", ".db", ".log", ".url",
            ".crdownload", ".part", ".tmp", ".DS_Store"}


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXT: return "image"
    if ext in DOC_EXT:   return "document"
    if ext in CODE_EXT:  return "code"
    if ext in VIDEO_EXT: return "video"
    if ext in AUDIO_EXT: return "audio"
    return "other"


def fmt_size(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.0f}{unit}" if unit == "B" else f"{b:.1f}{unit}"
        b /= 1024  # type: ignore[assignment]
    return f"{b:.1f}GB"


def scan(cutoff: datetime, quiet: bool) -> list[dict]:
    files: list[dict] = []
    seen_paths: set[str] = set()

    for root in SCAN_DIRS:
        if not root.exists():
            continue
        if not quiet:
            print(f"  scanning {root} ...", flush=True)

        try:
            all_files = list(root.rglob("*"))
        except PermissionError:
            continue

        for path in all_files:
            if not path.is_file():
                continue

            # Skip blacklisted directory names anywhere in the path
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue

            # Skip blacklisted extensions
            if path.suffix.lower() in SKIP_EXT:
                continue

            # Skip hidden files (Windows: starts with .)
            if path.name.startswith("."):
                continue

            str_path = str(path)
            if str_path in seen_paths:
                continue
            seen_paths.add(str_path)

            try:
                stat  = path.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                if mtime < cutoff:
                    continue

                files.append({
                    "path":    str_path,
                    "name":    path.name,
                    "type":    classify(path),
                    "size":    stat.st_size,
                    "size_hr": fmt_size(stat.st_size),
                    "mtime":   mtime.strftime("%Y-%m-%d %H:%M"),
                    "folder":  str(path.parent),
                })
            except (PermissionError, OSError):
                continue

    return sorted(files, key=lambda f: f["mtime"], reverse=True)


TYPE_LABEL = {
    "image": "Images",
    "document": "Documents",
    "code": "Code files",
    "video": "Videos",
    "audio": "Audio",
    "other": "Other files",
}

TYPE_EMOJI = {
    "image": "🖼",
    "document": "📄",
    "code": "💻",
    "video": "🎬",
    "audio": "🎵",
    "other": "📦",
}

CAP_PER_SECTION = 60  # keep the md file manageable


def write_md(files: list[dict]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Device file index — {now}",
        "",
        f"Auto-generated by `~/.claude/hooks/file_indexer.py` · **{len(files)} files** in the last {DAYS_BACK} days",
        "Directories scanned: Desktop · Downloads · Documents · Pictures",
        "",
        "---",
        "",
    ]

    by_type: dict[str, list[dict]] = {}
    for f in files:
        by_type.setdefault(f["type"], []).append(f)

    for t in ("image", "document", "code", "video", "audio", "other"):
        group = by_type.get(t, [])
        if not group:
            continue
        emoji = TYPE_EMOJI.get(t, "")
        label = TYPE_LABEL.get(t, t)
        lines.append(f"## {emoji} {label} ({len(group)})")
        lines.append("")
        for f in group[:CAP_PER_SECTION]:
            lines.append(f"- `{f['name']}` — `{f['folder']}` — {f['size_hr']} — {f['mtime'][:10]}")
        if len(group) > CAP_PER_SECTION:
            lines.append(f"- *(+{len(group) - CAP_PER_SECTION} more — see files-index.json for full list)*")
        lines.append("")

    lines += [
        "---",
        "",
        f"*Updated: {now} · Next auto-update: daily at 9 AM (Windows Task Scheduler)*",
    ]

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_json(files: list[dict]) -> None:
    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "days_back": DAYS_BACK,
        "count": len(files),
        "files": files,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Index recent device files for Claude memory")
    ap.add_argument("--quiet", "-q", action="store_true", help="suppress progress output")
    ap.add_argument("--clear-lock", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--days", type=int, default=DAYS_BACK, help=f"days back to scan (default {DAYS_BACK})")
    ap.add_argument("--if-stale", type=float, default=None, metavar="HOURS",
                    help="session-start mode: return at once; rebuild in the background only when the index is older than HOURS")
    args = ap.parse_args()

    # 2026-09-24: run synchronously as the SessionStart hook, the full scan took 131 s and
    # held every new Claude session on "Starting session…" (Praxis LIVE measured ~2.5 min).
    # The daily ClaudeFileIndexer task keeps it fresh; a session only kicks off a
    # background rebuild when the index is stale, and never waits for it.
    if args.if_stale is not None:
        try:
            age_h = (datetime.now().timestamp() - OUT_MD.stat().st_mtime) / 3600
        except OSError:
            age_h = float("inf")
        lock = MEMORY_DIR / "files-index.lock"
        try:
            busy = (datetime.now().timestamp() - lock.stat().st_mtime) < 900
        except OSError:
            busy = False
        if age_h >= args.if_stale and not busy:
            import subprocess, sys
            MEMORY_DIR.mkdir(parents=True, exist_ok=True)
            lock.write_text(str(os.getpid()), encoding="utf-8")
            exe = sys.executable
            wexe = os.path.join(os.path.dirname(exe), "pythonw.exe")
            flags = 0x00000008 | 0x08000000 if os.name == "nt" else 0  # DETACHED_PROCESS | CREATE_NO_WINDOW
            subprocess.Popen([wexe if os.path.exists(wexe) else exe, os.path.abspath(__file__), "--quiet", "--days", str(args.days), "--clear-lock"],
                             creationflags=flags, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
        return

    cutoff = datetime.now() - timedelta(days=args.days)

    if not args.quiet:
        print(f"Claude file indexer — scanning last {args.days} days ({cutoff.strftime('%Y-%m-%d')} onward)")

    files = scan(cutoff, args.quiet)

    if not args.quiet:
        by_type: dict[str, int] = {}
        for f in files:
            by_type[f["type"]] = by_type.get(f["type"], 0) + 1
        summary = "  " + "  ".join(f"{v} {k}s" for k, v in sorted(by_type.items()))
        print(f"Found {len(files)} files:{summary}")

    write_md(files)
    write_json(files)
    if "--clear-lock" in __import__("sys").argv:
        try:
            (MEMORY_DIR / "files-index.lock").unlink()
        except OSError:
            pass

    if not args.quiet:
        print(f"Index written -> {OUT_MD}")
        print(f"JSON  written -> {OUT_JSON}")


if __name__ == "__main__":
    main()
