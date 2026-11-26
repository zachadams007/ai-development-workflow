#!/usr/bin/env python3
"""Run a fully specified worker task on Codex, Cursor Agent, or Claude.

The caller remains the orchestrator and quality gate. This runner is synchronous;
use native managed tasks for long/background orchestration.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# Worker output often contains non-ASCII (e.g. U+2212); a cp1252 console would crash the write and lose the result.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def find_executable(*names):
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def find_codex():
    found = find_executable("codex")
    if found:
        return found
    npm = os.path.join(os.environ.get("APPDATA", ""), "npm")
    for name in ("codex.exe", "codex.cmd", "codex"):
        candidate = os.path.join(npm, name)
        if os.path.exists(candidate):
            return candidate
    return None


def find_claude():
    found = find_executable("claude")
    if found:
        return found
    npm = os.path.join(os.environ.get("APPDATA", ""), "npm")
    for name in ("claude.exe", "claude.cmd", "claude"):
        candidate = os.path.join(npm, name)
        if os.path.exists(candidate):
            return candidate
    return None


def find_cursor_agent():
    """Find a real Cursor Agent CLI, not the desktop `cursor` launcher."""
    return find_executable("cursor-agent", "agent")


GENERATE_PREAMBLE = """You are a worker handling a self-contained read-only task.
Do exactly what is requested. Do not modify files. Return the requested artifact
plus concise evidence that every acceptance criterion was addressed.

--- TASK ---
"""

EXECUTE_PREAMBLE = """You are a worker executing a fully specified task in an
isolated repository folder. Follow local instructions and neighboring conventions.
Stay inside scope; do not access secrets, push, deploy, purchase, message anyone,
or perform destructive actions unless the task explicitly authorizes it. Run the
specified verification and report changed files plus concrete evidence.

--- TASK ---
"""


def build_codex_command(args):
    executable = find_codex()
    if not executable:
        return None, "codex CLI not found", 127
    command = [
        executable,
        "exec",
        "--skip-git-repo-check",
        "-m",
        args.model,
        "-c",
        f'model_reasoning_effort="{args.effort}"',
        "-C",
        args.cd,
        "-c",
        f'sandbox_mode="{args.sandbox}"',
    ]
    return command, None, 0


def build_cursor_command(args, prompt):
    executable = find_cursor_agent()
    if not executable:
        return None, (
            "Cursor Agent CLI is not installed. Use live Cursor GUI automation "
            "(`cursor -n <folder>`) or another target."
        ), 127
    if args.mode == "generate":
        return None, (
            "Read-only Cursor headless mode is not safely verified on this host. "
            "Use Codex generate mode or an isolated Cursor GUI lane."
        ), 2
    return None, (
        "Cursor Agent headless effort control is not verified, so exact routing "
        "cannot be guaranteed. Use live Cursor GUI automation and visibly select "
        "the requested model and effort/mode."
    ), 2


def build_claude_command(args):
    executable = find_claude()
    if not executable:
        return None, "claude CLI not found", 127
    command = [
        executable,
        "-p",
        "--model",
        args.model,
        "--effort",
        args.effort,
        "--permission-mode",
        "plan" if args.mode == "generate" else "auto",
        "--add-dir",
        args.cd,
    ]
    return command, None, 0


def run_cursor_stream(command, cwd, timeout):
    """Stream Cursor JSON and require a terminal result event."""
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        output, _ = process.communicate()
        if output:
            sys.stdout.write(output)
        print(f"[offload] cursor timed out after {timeout}s", file=sys.stderr)
        return 124
    except FileNotFoundError:
        print("[offload] Cursor Agent executable disappeared", file=sys.stderr)
        return 127

    saw_result = False
    for line in output.splitlines(keepends=True):
        sys.stdout.write(line)
        try:
            event = json.loads(line)
            if isinstance(event, dict) and event.get("type") == "result":
                saw_result = True
        except json.JSONDecodeError:
            pass

    return_code = process.returncode
    if return_code != 0:
        return return_code
    if not saw_result:
        print(
            "[offload] cursor exited without a terminal result event; treat as incomplete",
            file=sys.stderr,
        )
        return 4
    return 0


def run_stdin_worker(command, prompt, cwd, timeout):
    try:
        completed = subprocess.run(
            command,
            input=prompt,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )
    except subprocess.TimeoutExpired:
        print(f"[offload] worker timed out after {timeout}s", file=sys.stderr)
        return 124
    except FileNotFoundError:
        print("[offload] worker executable not found", file=sys.stderr)
        return 127

    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--caller",
        choices=["codex", "cursor", "claude"],
        required=True,
        help="provider family of the orchestrator invoking this runner",
    )
    parser.add_argument(
        "--target", choices=["codex", "cursor", "claude"], required=True
    )
    parser.add_argument(
        "--mode", choices=["generate", "execute"], required=True
    )
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--effort",
        choices=["low", "medium", "high", "xhigh", "max", "ultra"],
        required=True,
        help="exact worker effort; Cursor headless is rejected until this can be verified",
    )
    parser.add_argument(
        "--cd", required=True, help="absolute existing worker folder/worktree"
    )
    parser.add_argument(
        "--sandbox",
        choices=["read-only", "workspace-write", "danger-full-access"],
        help="Codex sandbox override",
    )
    parser.add_argument("--prompt", help="prompt text; otherwise read stdin")
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    task = args.prompt if args.prompt is not None else sys.stdin.read()
    task = (task or "").strip()
    if not task:
        print("[offload] no prompt provided", file=sys.stderr)
        return 2
    if not os.path.isabs(args.cd):
        print(f"[offload] folder must be absolute: {args.cd}", file=sys.stderr)
        return 2
    if not os.path.isdir(args.cd):
        print(f"[offload] folder does not exist: {args.cd}", file=sys.stderr)
        return 2
    if args.caller == args.target:
        print(
            "[offload] caller and target must differ; use the caller's native "
            "task/subagent surface for same-provider fan-out",
            file=sys.stderr,
        )
        return 2
    if args.timeout < 1:
        print("[offload] timeout must be a positive integer", file=sys.stderr)
        return 2
    if args.target == "codex":
        if args.sandbox is None:
            print("[offload] --sandbox is required for Codex", file=sys.stderr)
            return 2
        if args.mode == "generate" and args.sandbox != "read-only":
            print("[offload] Codex generate mode requires --sandbox read-only", file=sys.stderr)
            return 2
    elif args.sandbox is not None:
        print("[offload] --sandbox applies only to Codex", file=sys.stderr)
        return 2
    if args.target == "claude" and args.effort == "ultra":
        print("[offload] Claude CLI does not support ultra effort", file=sys.stderr)
        return 2

    preamble = GENERATE_PREAMBLE if args.mode == "generate" else EXECUTE_PREAMBLE
    full_prompt = preamble + task

    if args.target == "codex":
        command, error, error_code = build_codex_command(args)
        use_stdin = True
    elif args.target == "cursor":
        command, error, error_code = build_cursor_command(args, full_prompt)
        use_stdin = False
    else:
        command, error, error_code = build_claude_command(args)
        use_stdin = True

    if error:
        print(f"[offload] {error}", file=sys.stderr)
        return error_code

    print(
        "[offload] "
        f"caller={args.caller} target={args.target} mode={args.mode} "
        f"model={args.model} effort={args.effort} folder={args.cd}",
        file=sys.stderr,
    )

    cwd = args.cd
    if args.target == "cursor":
        return run_cursor_stream(command, cwd, args.timeout)
    return run_stdin_worker(command, full_prompt if use_stdin else "", cwd, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
