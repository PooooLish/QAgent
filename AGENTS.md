# AGENTS.md

## Scope

These rules apply only to the QAgent task and supplement the workspace-root `AGENTS.md`. Follow the stricter rule if they differ.

## Working rules

- Read `README.md` and `task.md` before changing code.
- Treat this repository as a work in progress; keep changes small and reviewable.
- Use test-driven development for every behavior change or bug fix.
- Keep tests offline by default. Mock unavoidable service boundaries and never make real API calls in tests.
- Never store real API keys, tokens, passwords, uploaded private documents, or other private data.
- Put generated outputs in `outputs/`, temporary files in `tmp/`, and logs in `logs/`.
- Do not modify files outside this task directory.
- Do not commit Python bytecode, caches, virtual environments, local environment files, logs, temporary files, or uploaded documents.

## Verification

- Run `python -m pytest` for offline tests.
- Run an AST parse check when dependencies are unavailable.
- Report commands, results, and unresolved issues after each change.
