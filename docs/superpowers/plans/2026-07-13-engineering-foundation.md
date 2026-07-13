# QAgent Engineering Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum documentation, ignore rules, and offline test harness needed to maintain QAgent as an explicit work-in-progress task without changing application behavior.

**Architecture:** Keep project governance at the repository root and place characterization tests under `tests/`. Production dependencies remain in `requirements.txt`; pytest is isolated in `requirements-dev.txt`. Generated Python artifacts are ignored and removed from Git tracking.

**Tech Stack:** Python 3.10+, pytest 8, Git, Markdown

## Global Constraints

- Do not modify application behavior in this plan.
- Do not install dependencies or call external APIs.
- Do not add or expose real API keys, tokens, passwords, or private data.
- Tests must run without `OPENAI_API_KEY` and must not import `agent.llm`, `agent.workflow`, or `app`.
- Preserve the existing Git history and source layout.

---

### Task 1: Task governance and status

**Files:**
- Create: `AGENTS.md`
- Create: `task.md`

**Interfaces:**
- Consumes: workspace-root `AGENTS.md` rules and the approved design specification.
- Produces: the task-local operating rules and authoritative work-in-progress status used by future contributors.

- [ ] **Step 1: Create the task-local rules**

Create `AGENTS.md` with these requirements:

```markdown
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
```

- [ ] **Step 2: Create the work-in-progress task register**

Create `task.md` with this content:

```markdown
# QAgent task

## Status

Work in progress. The repository contains a Streamlit QA prototype with general QA, document ingestion, keyword retrieval, calculation, outline generation, and conversation memory.

## Current objective

Establish a maintainable engineering baseline before repairing application behavior.

## Known issues

- The math workflow branch does not return a result.
- Document summary requests are not routed to document QA unless the query explicitly mentions a PDF or document.
- LLM message construction can include an invalid `None` message and duplicates the system prompt.
- The README calculator example uses `^`, which the calculator does not support as exponentiation.
- Uploaded temporary files are not removed after ingestion.
- The reserved vector index module is empty.

## Current phase completion criteria

- Task-local rules and status documentation exist.
- Generated Python files and private local data are ignored.
- Offline characterization tests cover routing, calculation, chunking, and retrieval.
- Python bytecode is no longer tracked by Git.

## Verification commands

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest
git status --short
```

## Next phase

Repair each known behavior issue with a failing regression test followed by the smallest implementation change.
```

- [ ] **Step 3: Review the documents against workspace rules**

Run:

```powershell
Get-Content -Raw -Encoding UTF8 AGENTS.md
Get-Content -Raw -Encoding UTF8 task.md
```

Expected: both files render correctly, stay inside QAgent, and contain no weaker safety rule or placeholder.

- [ ] **Step 4: Check the documentation diff**

Run: `git diff --check -- AGENTS.md task.md`

Expected: exit code 0 and no output.

---

### Task 2: Ignore rules and development dependency boundary

**Files:**
- Create: `.gitignore`
- Create: `requirements-dev.txt`
- Create: `pytest.ini`
- Remove from Git tracking: `agent/__pycache__/`, `rag/__pycache__/`, `utils/__pycache__/`

**Interfaces:**
- Consumes: existing Python source layout and `requirements.txt`.
- Produces: deterministic ignore behavior and a single `python -m pytest` test entry point.

- [ ] **Step 1: Add the ignore policy**

Create `.gitignore`:

```gitignore
# Python bytecode and caches
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
env/

# Local environment and secrets
.env
.env.*
!.env.example

# Task-local generated files
logs/
tmp/
outputs/
data/uploads/*
!data/uploads/.gitkeep

# Editor and OS files
.idea/
.vscode/
.DS_Store
Thumbs.db
```

- [ ] **Step 2: Add the development dependency file**

Create `requirements-dev.txt`:

```text
-r requirements.txt
pytest>=8.0,<9.0
```

- [ ] **Step 3: Add pytest configuration**

Create `pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -q
```

- [ ] **Step 4: Verify ignore behavior before changing the index**

Run:

```powershell
git check-ignore -v agent/__pycache__/llm.cpython-310.pyc
git check-ignore -v data/uploads/example-private.txt
```

Expected: both paths match rules in `.gitignore`.

- [ ] **Step 5: Stop tracking generated bytecode**

Run:

```powershell
git rm -r --cached -- agent/__pycache__ rag/__pycache__ utils/__pycache__
```

Expected: only tracked cache directories are staged for removal; local files remain present and ignored.

- [ ] **Step 6: Verify the index cleanup**

Run:

```powershell
git ls-files | Select-String -Pattern '(^|/)__pycache__/|\.pyc$'
```

Expected: no output.

---

### Task 3: Offline characterization tests

**Files:**
- Create: `tests/test_router.py`
- Create: `tests/test_calculator.py`
- Create: `tests/test_ingest.py`
- Create: `tests/test_retrieve.py`

**Interfaces:**
- Consumes: `agent.router.route_query`, `utils.calculator.calculator`, `rag.ingest.chunk_text`, and `rag.retrieve.retrieve_chunks`.
- Produces: an offline baseline suite that documents currently supported behavior without importing OpenAI or Streamlit entry points.

- [ ] **Step 1: Write router characterization tests**

Create `tests/test_router.py`:

```python
from agent.router import route_query


def test_routes_arithmetic_to_calculator():
    assert route_query("2 + 3") == "calculator"


def test_routes_outline_request_to_outline():
    assert route_query("generate an outline") == "outline"


def test_routes_explicit_document_question_when_document_exists():
    assert route_query("这个文档讲了什么", has_document=True) == "document_qa"


def test_routes_plain_question_to_general_qa():
    assert route_query("What is machine learning?") == "general_qa"
```

- [ ] **Step 2: Write calculator characterization tests**

Create `tests/test_calculator.py`:

```python
from utils.calculator import calculator


def test_calculates_supported_arithmetic():
    assert calculator("计算 2**10 + 24") == "1048"


def test_rejects_function_calls():
    assert calculator("计算 __import__('os').getcwd()") == "计算失败，请检查表达式"
```

- [ ] **Step 3: Write chunking characterization tests**

Create `tests/test_ingest.py`:

```python
from rag.ingest import chunk_text


def test_returns_no_chunks_for_blank_text():
    assert chunk_text("   ") == []


def test_chunks_text_with_overlap():
    assert chunk_text("abcdefghij", chunk_size=4, overlap=1) == [
        "abcd",
        "defg",
        "ghij",
        "j",
    ]
```

- [ ] **Step 4: Write retrieval characterization tests**

Create `tests/test_retrieve.py`:

```python
from rag.retrieve import retrieve_chunks


def test_returns_matching_chunk_first():
    chunks = ["bananas are yellow", "apples are red", "grapes are purple"]
    assert retrieve_chunks("apples", chunks, top_k=1) == ["apples are red"]


def test_returns_no_chunks_for_blank_query():
    assert retrieve_chunks("", ["content"]) == []
```

- [ ] **Step 5: Run the tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest
```

Expected when pytest is available: `10 passed`. If pytest is unavailable, record `No module named pytest` as an environment limitation and do not install it without approval.

- [ ] **Step 6: Run dependency-free syntax verification**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
@'
from pathlib import Path
import ast

files = sorted(Path(".").rglob("*.py"))
for path in files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"AST_OK={len(files)}")
'@ | python -
```

Expected: exit code 0 and `AST_OK=19`.

---

### Task 4: Final scope and safety verification

**Files:**
- Verify: all files changed by Tasks 1–3

**Interfaces:**
- Consumes: the completed documentation, configuration, index cleanup, and offline tests.
- Produces: evidence that the implementation matches the approved design and contains no unrelated source changes.

- [ ] **Step 1: Verify required files**

Run:

```powershell
@('AGENTS.md', 'task.md', '.gitignore', 'requirements-dev.txt', 'pytest.ini', 'tests') | ForEach-Object {
    if (-not (Test-Path -LiteralPath $_)) { throw "Missing required path: $_" }
}
```

Expected: exit code 0 and no output.

- [ ] **Step 2: Verify no bytecode remains tracked**

Run:

```powershell
$tracked = git ls-files
if ($tracked -match '(^|/)__pycache__/|\.pyc$') { throw 'Tracked bytecode remains' }
```

Expected: exit code 0 and no output.

- [ ] **Step 3: Check for sensitive filenames without printing file contents**

Run:

```powershell
$unsafe = Get-ChildItem -Recurse -Force -File |
    Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.Name -match '(?i)(^\.env$|\.pem$|\.key$|id_rsa|token|secret|password|credential)' }
if ($unsafe) { $unsafe | Select-Object -ExpandProperty FullName; throw 'Sensitive-looking filenames found' }
```

Expected: exit code 0 and no output.

- [ ] **Step 4: Inspect the final diff and status**

Run:

```powershell
git diff --check
git status --short
git diff --stat
```

Expected: no whitespace errors; changes are limited to the approved governance, ignore, test, and cache-cleanup scope.

- [ ] **Step 5: Commit the engineering foundation**

Run:

```powershell
git add -- AGENTS.md task.md .gitignore requirements-dev.txt pytest.ini tests
git commit -m "chore: establish engineering foundation"
```

Expected: one commit containing only the approved engineering foundation and staged cache removals.
