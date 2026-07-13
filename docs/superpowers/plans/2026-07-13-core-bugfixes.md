# QAgent Core Bug Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair five confirmed QAgent defects with isolated offline regression tests and minimal production changes.

**Architecture:** Preserve the current router → workflow → LLM structure. Centralize summary intent in the router, keep calculator normalization at its public boundary, and move uploaded-file lifetime management into `utils/file_utils.py`. All external boundaries are replaced by fakes in tests.

**Tech Stack:** Python 3.10+, pytest 8, OpenAI Python SDK, Streamlit

## Global Constraints

- Do not implement `rag/index.py` or add new product features.
- Do not make real OpenAI calls or start Streamlit during tests.
- Do not store real API keys, uploaded documents, logs, caches, or temporary files.
- Write and run each regression test before changing its production code.
- Keep the existing public route names and result dictionary keys.
- Limit business-source changes to `agent/llm.py`, `agent/router.py`, `agent/tools.py`, `agent/workflow.py`, `utils/calculator.py`, `utils/file_utils.py`, and `app.py`.

---

### Task 1: Return a complete result from the math workflow

**Files:**
- Modify: `agent/workflow.py:56`
- Create: `tests/test_workflow.py`

**Interfaces:**
- Consumes: `GeneralQAAgent.run(query: str, chunks: list[str], memory) -> dict`.
- Produces: math results with `route`, `answer`, `retrieval_mode`, and `retrieved_chunks`.

- [ ] **Step 1: Write the failing regression test**

Create `tests/test_workflow.py`:

```python
import sys
import types

openai_stub = types.ModuleType("openai")
openai_stub.OpenAI = object
sys.modules.setdefault("openai", openai_stub)

from agent.workflow import GeneralQAAgent


class FakeLLM:
    def generate(self, prompt, system_prompt=None):
        return "x² 的导数是 2x"


class FakeMemory:
    def get_history_text(self):
        return ""


def test_math_route_returns_complete_result():
    agent = GeneralQAAgent.__new__(GeneralQAAgent)
    agent.llm = FakeLLM()

    result = agent.run("求 x² 的导数", [], FakeMemory())

    assert result == {
        "route": "math",
        "answer": "x² 的导数是 2x",
        "retrieval_mode": "none",
        "retrieved_chunks": [],
    }
```

- [ ] **Step 2: Verify the test fails for the expected reason**

Run: `python -m pytest tests/test_workflow.py::test_math_route_returns_complete_result -v`

Expected: FAIL because `result` is `None`.

- [ ] **Step 3: Add the minimal math return value**

After `answer = self.llm.generate(...)` in the math branch, add:

```python
            return {
                "route": route,
                "answer": answer,
                "retrieval_mode": "none",
                "retrieved_chunks": [],
            }
```

- [ ] **Step 4: Verify the focused and full suites**

Run:

```powershell
python -m pytest tests/test_workflow.py -v
python -m pytest
```

Expected: focused test passes; full suite reports 11 passing tests.

- [ ] **Step 5: Commit the workflow fix**

```powershell
git add -- agent/workflow.py tests/test_workflow.py
git commit -m "fix: return math workflow result"
```

---

### Task 2: Route document summaries consistently

**Files:**
- Modify: `agent/router.py`
- Modify: `agent/tools.py`
- Modify: `tests/test_router.py`

**Interfaces:**
- Produces: `SUMMARY_KEYWORDS: tuple[str, ...]` and `is_summary_query(query: str) -> bool` from `agent.router`.
- Consumes: `agent.tools.build_document_context()` reuses `is_summary_query` from the router.

- [ ] **Step 1: Add failing routing tests**

Append to `tests/test_router.py`:

```python
def test_routes_summary_request_to_document_qa_when_document_exists():
    assert route_query("总结主要内容", has_document=True) == "document_qa"


def test_keeps_calculator_priority_for_summary_text_with_arithmetic():
    assert route_query("总结 2 + 2", has_document=True) == "calculator"
```

- [ ] **Step 2: Verify the summary test fails**

Run: `python -m pytest tests/test_router.py -v`

Expected: one failure where `general_qa` is returned instead of `document_qa`; the priority test passes.

- [ ] **Step 3: Centralize summary intent and update routing**

At the top of `agent/router.py`, add:

```python
SUMMARY_KEYWORDS = (
    "介绍",
    "总结",
    "概述",
    "主要内容",
    "讲什么",
    "说了什么",
    "摘要",
)


def is_summary_query(query: str) -> bool:
    normalized = query.strip().lower()
    return bool(normalized) and any(
        keyword in normalized for keyword in SUMMARY_KEYWORDS
    )
```

In `route_query()`, after the outline check and before the existing explicit-document check, add:

```python
    if has_document and is_summary_query(q):
        return "document_qa"
```

- [ ] **Step 4: Remove the duplicate summary list from tools**

Replace the local `SUMMARY_KEYWORDS` and `is_summary_query()` in `agent/tools.py` with:

```python
from agent.router import is_summary_query
```

Keep the existing RAG and utility imports unchanged.

- [ ] **Step 5: Verify routing and document-context tests**

Run:

```powershell
python -m pytest tests/test_router.py -v
python -m pytest
```

Expected: all tests pass; full suite reports 13 passing tests.

- [ ] **Step 6: Commit the routing fix**

```powershell
git add -- agent/router.py agent/tools.py tests/test_router.py
git commit -m "fix: route document summary requests"
```

---

### Task 3: Build valid OpenAI messages

**Files:**
- Modify: `agent/llm.py`
- Create: `tests/test_llm.py`

**Interfaces:**
- Produces: `build_messages(prompt: str, system_prompt: str | None = None) -> list[dict[str, str]]`.
- Consumes: `LLMClient.generate()` sends the helper output to `chat.completions.create()`.

- [ ] **Step 1: Write failing message-construction tests**

Create `tests/test_llm.py`:

```python
import sys
import types

openai_stub = types.ModuleType("openai")
openai_stub.OpenAI = object
sys.modules.setdefault("openai", openai_stub)

from agent.llm import LLMClient


class FakeCompletions:
    def __init__(self):
        self.messages = None

    def create(self, *, model, messages):
        self.messages = messages
        message = types.SimpleNamespace(content="answer")
        choice = types.SimpleNamespace(message=message)
        return types.SimpleNamespace(choices=[choice])


def make_client():
    client = LLMClient.__new__(LLMClient)
    completions = FakeCompletions()
    client.client = types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=completions)
    )
    client.model = "test-model"
    return client, completions


def test_generate_sends_system_and_user_messages_without_duplication():
    client, completions = make_client()
    assert client.generate("question", "instructions") == "answer"
    assert completions.messages == [
        {"role": "system", "content": "instructions"},
        {"role": "user", "content": "question"},
    ]


def test_generate_omits_system_message_when_not_provided():
    client, completions = make_client()
    client.generate("question")
    assert completions.messages == [
        {"role": "user", "content": "question"},
    ]
```

- [ ] **Step 2: Verify both tests fail against the current implementation**

Run: `python -m pytest tests/test_llm.py -v`

Expected: failures show duplicated system text and a `None` message.

- [ ] **Step 3: Implement the message helper and use it**

In `agent/llm.py`, add above `LLMClient`:

```python
def build_messages(
    prompt: str, system_prompt: str | None = None
) -> list[dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages
```

Replace `full_input` construction and the inline `messages` list in `generate()` with:

```python
        response = self.client.chat.completions.create(
            model=self.model,
            messages=build_messages(prompt, system_prompt),
        )
```

- [ ] **Step 4: Verify the focused and full suites**

Run:

```powershell
python -m pytest tests/test_llm.py -v
python -m pytest
```

Expected: all tests pass; full suite reports 15 passing tests.

- [ ] **Step 5: Commit the LLM fix**

```powershell
git add -- agent/llm.py tests/test_llm.py
git commit -m "fix: construct valid LLM messages"
```

---

### Task 4: Support the documented exponent syntax

**Files:**
- Modify: `utils/calculator.py`
- Modify: `tests/test_calculator.py`

**Interfaces:**
- Consumes: `calculator(expr: str) -> str`.
- Produces: `^` is treated as exponentiation before AST parsing; the operator whitelist remains unchanged.

- [ ] **Step 1: Replace the calculator success test with the README input**

Change `test_calculates_supported_arithmetic()` in `tests/test_calculator.py` to:

```python
def test_calculates_documented_exponent_syntax():
    assert calculator("计算 2^10 + 24") == "1048"
```

- [ ] **Step 2: Verify the test fails**

Run: `python -m pytest tests/test_calculator.py -v`

Expected: FAIL because the result is `计算失败，请检查表达式`.

- [ ] **Step 3: Normalize the public expression input**

In `calculator()`, replace the current normalization line with:

```python
    expr = expr.replace("计算", "").replace("^", "**").strip()
```

- [ ] **Step 4: Verify success and safety behavior**

Run:

```powershell
python -m pytest tests/test_calculator.py -v
python -m pytest
```

Expected: exponent and malicious-expression tests pass; full suite reports 15 passing tests.

- [ ] **Step 5: Commit the calculator fix**

```powershell
git add -- utils/calculator.py tests/test_calculator.py
git commit -m "fix: support documented exponent syntax"
```

---

### Task 5: Clean uploaded temporary files on every path

**Files:**
- Modify: `utils/file_utils.py`
- Modify: `app.py`
- Create: `tests/test_file_utils.py`

**Interfaces:**
- Produces: `load_uploaded_document(uploaded_file, loader=load_document_text) -> str`.
- Consumes: an uploaded object with `.name` and `.read()`, plus a loader callable accepting the generated path.

- [ ] **Step 1: Write failing success and error cleanup tests**

Create `tests/test_file_utils.py`:

```python
from pathlib import Path

import pytest

from utils.file_utils import load_uploaded_document


class FakeUpload:
    name = "notes.txt"

    def read(self):
        return b"hello"


def test_removes_temporary_file_after_successful_load():
    seen_path = None

    def loader(path):
        nonlocal seen_path
        seen_path = Path(path)
        assert seen_path.exists()
        return "loaded"

    assert load_uploaded_document(FakeUpload(), loader=loader) == "loaded"
    assert seen_path is not None
    assert not seen_path.exists()


def test_removes_temporary_file_when_loader_raises():
    seen_path = None

    def loader(path):
        nonlocal seen_path
        seen_path = Path(path)
        raise ValueError("bad document")

    with pytest.raises(ValueError, match="bad document"):
        load_uploaded_document(FakeUpload(), loader=loader)

    assert seen_path is not None
    assert not seen_path.exists()
```

- [ ] **Step 2: Verify collection fails because the helper does not exist**

Run: `python -m pytest tests/test_file_utils.py -v`

Expected: ERROR importing `load_uploaded_document`.

- [ ] **Step 3: Implement owned temporary-file cleanup**

In `utils/file_utils.py`, add imports and the helper:

```python
from collections.abc import Callable

from rag.ingest import load_document_text


def load_uploaded_document(
    uploaded_file,
    loader: Callable[[str], str] = load_document_text,
) -> str:
    temp_path = Path(save_temp_file(uploaded_file))
    try:
        return loader(str(temp_path))
    finally:
        temp_path.unlink(missing_ok=True)
```

- [ ] **Step 4: Replace direct temporary-file management in the app**

In `app.py`:

- Remove `import tempfile`.
- Change the RAG import to `from rag.ingest import chunk_text`.
- Add `from utils.file_utils import load_uploaded_document`.
- Replace the `NamedTemporaryFile` block and `load_document_text(tmp_path)` call with:

```python
        text = load_uploaded_document(uploaded_file)
```

- [ ] **Step 5: Verify cleanup tests and the full suite**

Run:

```powershell
python -m pytest tests/test_file_utils.py -v
python -m pytest
```

Expected: both cleanup paths pass; full suite reports 17 passing tests.

- [ ] **Step 6: Commit the upload cleanup fix**

```powershell
git add -- utils/file_utils.py app.py tests/test_file_utils.py
git commit -m "fix: clean uploaded temporary files"
```

---

### Task 6: Update task status and perform final verification

**Files:**
- Modify: `task.md`

**Interfaces:**
- Consumes: completed fixes and verification evidence.
- Produces: task status that distinguishes repaired defects from the deferred vector index.

- [ ] **Step 1: Update the task register**

Replace `## Known issues` and the current phase sections in `task.md` with:

```markdown
## Completed fixes

- Math workflow returns a complete result dictionary.
- Document summary requests use document QA when a document is loaded.
- LLM requests contain only valid, non-duplicated messages.
- The calculator accepts the documented `^` exponent syntax.
- Uploaded temporary files are removed after successful or failed parsing.

## Remaining work

- Implement and evaluate the reserved vector index only when semantic retrieval becomes a confirmed requirement.
- Add end-to-end Streamlit coverage when a stable UI contract is defined.

## Current phase completion criteria

- Every repaired defect has an offline regression test.
- All offline tests pass without API calls.
- Python bytecode, uploaded documents, secrets, logs, and temporary files remain untracked.

## Verification commands

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest
git status --short
```

## Next phase

Evaluate retrieval quality and decide whether the reserved vector index is necessary.
```

- [ ] **Step 2: Run the full test suite and AST parse**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest
@'
from pathlib import Path
import ast

files = sorted(Path(".").rglob("*.py"))
for path in files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"AST_OK={len(files)}")
'@ | python -
```

Expected: 17 tests pass and all 22 Python files parse.

- [ ] **Step 3: Verify scope, whitespace, and sensitive filenames**

Run:

```powershell
git diff --check
git status --short
$unsafe = Get-ChildItem -Recurse -Force -File |
    Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.Name -match '(?i)(^\.env$|\.pem$|\.key$|id_rsa|token|secret|password|credential)' }
if ($unsafe) { $unsafe | Select-Object -ExpandProperty FullName; throw 'Sensitive-looking filenames found' }
```

Expected: no whitespace errors or sensitive-looking files; only `task.md` remains uncommitted after the five fix commits.

- [ ] **Step 4: Commit the status update**

```powershell
git add -- task.md
git commit -m "docs: record completed core fixes"
```

- [ ] **Step 5: Verify the repository is clean**

Run:

```powershell
python -m pytest
git status --short --branch
```

Expected: 17 tests pass and the branch has no uncommitted changes.
