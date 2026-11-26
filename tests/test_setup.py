"""Written for this public copy; not part of the original setup. Offline, standard library only.

    python -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "versioning"))
import restore  # noqa: E402
import snapshot  # noqa: E402

# Assembled at run time so that no credential-shaped string exists in this file.
FAKE = {
    "Anthropic API key": "sk-" + "ant-" + "x" * 24,
    "OpenAI-style API key": "sk-" + "a1" * 20,
    "GitHub token": "gh" + "p_" + "A1" * 18,
    "AWS access key id": "AK" + "IA" + "A1B2C3D4E5F6G7H8",
    "JWT": ".".join(["ey" + "J" * 20, "a" * 24, "b" * 24]),
    "private key block": "-----BEGIN " + "RSA PRIVATE" + " KEY-----",
}


def quiet(fn):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        return fn(), out.getvalue()


class Scanner(unittest.TestCase):
    def test_each_pattern_fires_on_its_own_sample(self):
        for label, token in FAKE.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                Path(tmp, "note.md").write_text(f"pasted by accident: {token}\n", encoding="utf-8")
                self.assertIn(label, {found for _, found in snapshot.scan_for_secrets(tmp)})

    def test_every_pattern_has_a_sample(self):
        self.assertEqual({label for _, label in snapshot.SECRET_PATTERNS}, set(FAKE))

    def test_prose_about_keys_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "note.md").write_text("Keys live in the secrets folder. Prefix: sk-. Never commit them.", encoding="utf-8")
            self.assertEqual(snapshot.scan_for_secrets(tmp), [])


class Snapshot(unittest.TestCase):
    def run_snapshot(self, content):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        src = Path(tmp.name, "live.md")
        src.write_text(content, encoding="utf-8")
        dest = Path(tmp.name, "surfaces")
        calls = []
        with mock.patch.object(snapshot, "MANIFEST", [(str(src), "live.md", "file")]), \
                mock.patch.object(snapshot, "DEST_ROOT", str(dest)), \
                mock.patch.object(snapshot, "git", side_effect=lambda *a, **k: calls.append(a) or ""), \
                mock.patch.object(sys, "argv", ["snapshot.py"]):
            code, _ = quiet(snapshot.main)
        return code, calls

    def test_a_credential_stops_the_run_before_git_is_called(self):
        code, calls = self.run_snapshot("token " + FAKE["GitHub token"])
        self.assertEqual(code, 2)
        self.assertEqual(calls, [])

    def test_a_clean_file_reaches_git_add(self):
        code, calls = self.run_snapshot("plain rules")
        self.assertEqual(code, 0)
        self.assertEqual(calls[0], ("add", "-A"))

    def test_forbidden_paths_are_refused_even_when_listed(self):
        home = str(Path.home())
        for rel in (".claude/secrets/keys.env", ".claude/.credentials.json", ".codex/auth.json"):
            self.assertTrue(snapshot.forbidden(f"{home}/{rel}"), rel)
        self.assertFalse(snapshot.forbidden(f"{home}/.claude/CLAUDE.md"))

    def test_trees_copy_only_allowed_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp, "skills")
            (src / "node_modules").mkdir(parents=True)
            (src / "SKILL.md").write_text("ok", encoding="utf-8")
            (src / "state.sqlite").write_text("no", encoding="utf-8")
            (src / "node_modules" / "pkg.md").write_text("no", encoding="utf-8")
            result = snapshot.copy_tree(str(src), str(Path(tmp, "out")))
            copied = sorted(p.name for p in Path(tmp, "out").rglob("*") if p.is_file())
        self.assertEqual(copied, ["SKILL.md"])
        self.assertEqual((result["new"], result["skipped"]), (1, 1))


class Restore(unittest.TestCase):
    def run_restore(self, *argv):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        live, dest = Path(tmp.name, "live.md"), Path(tmp.name, "surfaces")
        dest.mkdir()
        live.write_text("edited badly", encoding="utf-8")
        (dest / "live.md").write_text("good copy", encoding="utf-8")
        with mock.patch.object(restore, "MANIFEST", [(str(live), "live.md", "file")]), \
                mock.patch.object(restore, "DEST_ROOT", str(dest)), \
                mock.patch.object(sys, "argv", ["restore.py", *argv]):
            quiet(restore.main)
        return live, list(Path(tmp.name).glob("live.md.pre-restore-*"))

    def test_default_is_a_dry_run(self):
        live, backups = self.run_restore()
        self.assertEqual(live.read_text(encoding="utf-8"), "edited badly")
        self.assertEqual(backups, [])

    def test_apply_restores_and_keeps_a_backup(self):
        live, backups = self.run_restore("--apply")
        self.assertEqual(live.read_text(encoding="utf-8"), "good copy")
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "edited badly")


class Offload(unittest.TestCase):
    BASE = {"--caller": "claude", "--target": "codex", "--mode": "generate", "--model": "m", "--effort": "high",
            "--sandbox": "read-only", "--prompt": "task"}

    def offload(self, cd=None, **over):
        args = {**self.BASE, "--cd": cd or tempfile.gettempdir(), **{f"--{k}": v for k, v in over.items()}}
        cmd = [sys.executable, str(ROOT / "skills" / "offload" / "offload.py")]
        for k, v in args.items():
            if v is not None:
                cmd += [k, v]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60,
                           env={**os.environ, "PATH": "", "APPDATA": ""})
        return r.returncode, r.stderr

    def test_a_tool_cannot_offload_to_itself(self):
        code, err = self.offload(caller="codex")
        self.assertEqual(code, 2)
        self.assertIn("must differ", err)

    def test_relative_folder_is_rejected(self):
        code, err = self.offload(cd="work")
        self.assertEqual(code, 2)
        self.assertIn("must be absolute", err)

    def test_read_only_task_cannot_take_a_writable_sandbox(self):
        code, err = self.offload(sandbox="workspace-write")
        self.assertEqual(code, 2)
        self.assertIn("read-only", err)

    def test_unverifiable_effort_is_refused(self):
        code, err = self.offload(target="cursor", sandbox=None)
        self.assertNotEqual(code, 0)
        self.assertIn("Cursor", err)

    def test_missing_cli_reports_127(self):
        code, err = self.offload()
        self.assertEqual(code, 127)
        self.assertIn("not found", err)


class Hooks(unittest.TestCase):
    def run_hook(self, tool, name, prompt="hello", cwd="/tmp"):
        r = subprocess.run([sys.executable, str(ROOT / "hooks" / tool / f"{name}.py")], capture_output=True, text=True,
                           input=json.dumps({"prompt": prompt, "cwd": cwd}), encoding="utf-8", timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_both_tools_receive_twelve_numbered_rules(self):
        for tool, name in (("claude-code", "preference_enforcer"), ("codex", "preference_enforcer_codex")):
            out = self.run_hook(tool, name)
            out = json.loads(out)["hookSpecificOutput"]["additionalContext"] if tool == "codex" else out
            self.assertEqual([int(n) for n in re.findall(r"(?m)^(\d+)\. ", out)], list(range(1, 13)), tool)

    def test_a_hook_survives_malformed_input(self):
        for name in ("preference_enforcer", "skill_check", "task_ledger_reminder"):
            r = subprocess.run([sys.executable, str(ROOT / "hooks" / "claude-code" / f"{name}.py")], input="not json",
                               capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(r.returncode, 0)
            self.assertTrue(r.stdout.strip())

    def test_multi_part_prompts_get_the_longer_reminder(self):
        short = self.run_hook("claude-code", "task_ledger_reminder", "fix the parser")
        multi = self.run_hook("claude-code", "task_ledger_reminder", "- fix the parser\n- add a test\n- update the docs")
        self.assertGreater(len(multi), len(short))

    def test_mission_control_line_depends_on_the_folder(self):
        self.assertNotIn("MISSION CONTROL", self.run_hook("claude-code", "preference_enforcer", cwd="/work/app"))
        self.assertIn("MISSION CONTROL", self.run_hook("claude-code", "preference_enforcer", cwd="/work/command-deck"))


if __name__ == "__main__":
    unittest.main()
