# QAgent Rule Router Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve deterministic routing accuracy while preserving `route_query(query: str, has_document: bool = False) -> str` for all existing callers.

**Architecture:** Split intent recognition into pure helper functions, then keep `route_query()` as a small priority coordinator. Use strict lexical arithmetic validation, contextual document terms, and table-driven pytest coverage. The helpers remain reusable for a later structured `RouteDecision` implementation.

**Tech Stack:** Python 3.10, standard-library `re`, pytest 8

## Global Constraints

- Do not add an LLM router, Agent loop, confidence object, network dependency, or new route name.
- Preserve the five string routes: `calculator`, `math`, `outline`, `document_qa`, `general_qa`.
- Do not modify `agent/workflow.py` or `app.py`.
- Use failing tests before each production change.
- Keep all routing decisions deterministic and offline.
- Update both public README files and the ignored private handbook after behavior changes.

---

### Task 1: Characterize arithmetic intent and reject false positives

**Files:**
- Modify: `tests/test_router.py`
- Modify: `agent/router.py`

**Interfaces:**
- Produces: `normalize_query(query: str) -> str`
- Produces: `is_calculator_query(query: str) -> bool`
- Preserves: `route_query(query: str, has_document: bool = False) -> str`

- [ ] **Step 1: Add table-driven calculator helper tests**

Extend imports in `tests/test_router.py` with `pytest`, `normalize_query`, and `is_calculator_query`. Add:

```python
@pytest.mark.parametrize(
    "query",
    [
        "2 + 3",
        "计算 2^10 + 24",
        "算一下 (12.5 - 2.5) / 2",
        "请帮我计算 -4 * (3 + 2)",
        "2 + 3 等于多少？",
        "10 % 3",
    ],
)
def test_recognizes_calculator_queries(query):
    assert is_calculator_query(query)


@pytest.mark.parametrize(
    "query",
    [
        "https://example.com/docs",
        "解释 client/server 架构",
        "什么是 A/B 测试",
        "state-of-the-art 是什么意思",
        "版本 2.0",
        "2026-07-13",
        "42",
        "",
    ],
)
def test_rejects_non_calculator_queries(query):
    assert not is_calculator_query(query)


def test_normalizes_query_once():
    assert normalize_query("  Generate AN OUTLINE  ") == "generate an outline"
```

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_router.py -v`

Expected: collection fails because the new helper functions do not exist.

- [ ] **Step 3: Implement normalization and strict calculator recognition**

In `agent/router.py`, import `re` and add:

```python
CALCULATOR_PREFIX_PATTERN = re.compile(
    r"^(?:(?:请|帮我|请帮我)\s*)?(?:计算|算一下|算一算)\s*"
)
CALCULATOR_SUFFIX_PATTERN = re.compile(
    r"\s*(?:等于多少|是多少|结果是多少|结果|的结果)[？?]?$"
)
ARITHMETIC_EXPRESSION_PATTERN = re.compile(r"[0-9\s.+\-*/^%()]+")


def normalize_query(query: str) -> str:
    return query.strip().lower()


def is_calculator_query(query: str) -> bool:
    candidate = CALCULATOR_PREFIX_PATTERN.sub("", normalize_query(query))
    candidate = CALCULATOR_SUFFIX_PATTERN.sub("", candidate).strip()
    return (
        bool(re.search(r"\d", candidate))
        and bool(re.search(r"[+\-*/^%]", candidate))
        and ARITHMETIC_EXPRESSION_PATTERN.fullmatch(candidate) is not None
    )
```

Replace the current calculator condition in `route_query()` with `is_calculator_query(q)` while retaining current priority for this task.

- [ ] **Step 4: Verify GREEN and regression safety**

Run:

```powershell
python -m pytest tests/test_router.py -v
python -m pytest
```

Expected: helper tests pass, URL and textual slash/hyphen cases route to `general_qa`, and the full suite passes.

---

### Task 2: Add math, document, and outline helpers with explicit priority

**Files:**
- Modify: `tests/test_router.py`
- Modify: `agent/router.py`

**Interfaces:**
- Produces: `is_math_query(query: str) -> bool`
- Produces: `is_document_query(query: str, has_document: bool) -> bool`
- Produces: `is_outline_query(query: str) -> bool`
- Preserves: existing summary helper and string route API.

- [ ] **Step 1: Add direct helper and priority tests**

Extend imports and add parameterized cases covering:

```python
@pytest.mark.parametrize("query", ["求 x 的导数", "计算 x 的导数", "解释这个积分", "这个极限是多少"])
def test_recognizes_math_queries(query):
    assert is_math_query(query)


@pytest.mark.parametrize(
    "query",
    [
        "这个文档讲了什么",
        "总结主要内容",
        "作者的主要观点是什么",
        "本文的结论是什么",
        "这篇文章有哪些限制",
        "这份材料讲了什么",
        "第二章节讨论什么",
        "实验使用了什么数据",
    ],
)
def test_recognizes_document_queries_when_document_exists(query):
    assert is_document_query(query, has_document=True)


@pytest.mark.parametrize("query", ["作者是谁", "结论是什么", "这篇文章讲什么"])
def test_does_not_route_document_references_without_document(query):
    assert not is_document_query(query, has_document=False)


def test_document_outline_uses_document_route_when_document_exists():
    assert route_query("给这份文档生成提纲", has_document=True) == "document_qa"


def test_document_outline_falls_back_to_outline_without_document():
    assert route_query("给这份文档生成提纲", has_document=False) == "outline"


def test_math_has_priority_over_calculation_control_word():
    assert route_query("计算 x 的导数") == "math"
```

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_router.py -v`

Expected: collection fails for missing helper imports or new priority assertions fail against the old route order.

- [ ] **Step 3: Implement helpers and constants**

Add tuples:

```python
MATH_KEYWORDS = ("积分", "导数", "极限")
OUTLINE_KEYWORDS = ("提纲", "outline")
DOCUMENT_EXPLICIT_TERMS = ("文档", "pdf", "文章", "材料", "论文", "文件")
DOCUMENT_REFERENCE_TERMS = (
    "作者",
    "本文",
    "这篇",
    "这份",
    "其中",
    "章节",
    "结论",
    "实验",
)


def contains_any(query: str, terms: tuple[str, ...]) -> bool:
    return any(term in query for term in terms)


def is_math_query(query: str) -> bool:
    return contains_any(normalize_query(query), MATH_KEYWORDS)


def is_outline_query(query: str) -> bool:
    return contains_any(normalize_query(query), OUTLINE_KEYWORDS)


def is_document_query(query: str, has_document: bool) -> bool:
    if not has_document:
        return False
    normalized = normalize_query(query)
    return (
        is_summary_query(normalized)
        or contains_any(normalized, DOCUMENT_EXPLICIT_TERMS)
        or contains_any(normalized, DOCUMENT_REFERENCE_TERMS)
    )
```

Refactor `route_query()` to the approved order:

```python
def route_query(query: str, has_document: bool = False) -> str:
    normalized = normalize_query(query)

    if is_math_query(normalized):
        return "math"
    if is_calculator_query(normalized):
        return "calculator"
    if is_document_query(normalized, has_document):
        return "document_qa"
    if is_outline_query(normalized):
        return "outline"
    return "general_qa"
```

- [ ] **Step 4: Verify 30+ samples and the full suite**

Run:

```powershell
python -m pytest tests/test_router.py -v
python -m pytest
```

Expected: at least 35 router test cases pass and the full suite passes.

- [ ] **Step 5: Commit the Router implementation**

Run:

```powershell
git add -- agent/router.py tests/test_router.py
git commit -m "fix: harden deterministic intent routing"
```

Expected: one commit limited to Router source and tests.

---

### Task 3: Synchronize public and private documentation

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify, ignored and never staged: `docs/private/QAgent项目维护手册.md`

**Interfaces:**
- Consumes: the new verified route priority and terms.
- Produces: documentation consistent with behavior while preserving private-file confidentiality.

- [ ] **Step 1: Update English Router documentation**

Change the route table and limitation text to describe:

1. math keywords;
2. valid arithmetic expressions;
3. document references when a document is loaded;
4. ordinary outlines;
5. general QA.

Mention that slash and hyphen characters alone no longer imply calculator intent.

- [ ] **Step 2: Apply the same facts in Chinese**

Update `README.zh-CN.md` with the identical order, examples, and limitations in Chinese.

- [ ] **Step 3: Update the ignored private handbook locally**

Update the Router priority, module explanation, known limitations, change-trigger notes, baseline commit, and maintenance record. Do not stage this file.

- [ ] **Step 4: Verify documentation and privacy**

Run:

```powershell
git check-ignore -v -- 'docs/private/QAgent项目维护手册.md'
git ls-files -- 'docs/private/QAgent项目维护手册.md'
git diff --check -- README.md README.zh-CN.md
```

Expected: private file is ignored and untracked; both public README files have no whitespace errors.

- [ ] **Step 5: Commit public documentation only**

Run:

```powershell
git add -- README.md README.zh-CN.md
git commit -m "docs: document hardened router behavior"
```

Expected: the commit contains only the two public README files.

---

### Task 4: Final verification

**Files:**
- Verify: all changes from Tasks 1–3

**Interfaces:**
- Consumes: implementation, tests, and synchronized documentation.
- Produces: completion evidence without adding private artifacts.

- [ ] **Step 1: Run all tests and AST parsing**

Run `python -m pytest` with bytecode disabled, then parse every `*.py` file with `ast.parse`.

Expected: all tests pass and all Python files parse.

- [ ] **Step 2: Verify compatibility**

Run a short Python check asserting that every `route_query()` result is a `str` and belongs to the existing five-route set.

Expected: no new return type or route name.

- [ ] **Step 3: Verify scope and confidentiality**

Run `git status --short --branch`, `git diff --check`, `git ls-files` for the private handbook, and a sensitive-looking filename scan.

Expected: tracked workspace is clean, the private handbook is absent from Git, and no sensitive-looking file is introduced.
