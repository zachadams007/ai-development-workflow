# Provenance

This repository is a public copy of selected files from two private repositories. It has fresh history because the private ones contain local paths and working notes.

| Part | Source |
|---|---|
| `hooks`, `rules`, `skills`, `versioning` | Configuration repository at `0b8f82a`, 7 commits from 2026-07-26 to 2026-10-11 |
| `state/refresh-state.py` | Mission-control repository at `d88c5c7`, 2026-07-26 |

Files were passed through a scripted allowlist, redaction and deny-list check.

## Files written for this copy

- `README.md`, `PROVENANCE.md`, `.gitignore`
- `tests/test_setup.py`, `.github/workflows/ci.yml`
- `examples/claude-code-settings.json`, the hook registration with a generic home path

Everything else is the setup as it runs.

## Left out

- The active work board, session notes, account procedures and slash commands
- Third-party skills, three skills that contain trading content, and short wrapper skills
- Full tool settings

## Changed

- Home-directory paths are `~` or `~/workspace`.
- `state/refresh-state.py` is `src/refresh-state.py` in its own repository, which is the path the rules use. The script rewrites a `START-HERE.md` in that repository, and that file is not published.
- Sentences about accounts and subscriptions are removed, and private repository addresses are placeholders. The rules keep the author's first name because the prompts are written that way.
- One sentence in the autonomy skill was reworded to state that the session the user opens is the orchestrator, matching the agreement.
- Em dashes in code comments are normalised to hyphens.

## Credit

`skills/premium-frontend-ui` adapts its quality taxonomy from [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT licence).
