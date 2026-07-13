# QAgent Private Maintenance Handbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a detailed, maintainable Chinese QAgent handbook that remains local and cannot be committed accidentally.

**Architecture:** Add a tracked ignore boundary before creating the private artifact. Build one UTF-8 Markdown handbook from verified repository facts, then validate its structure, confidentiality, accuracy, and ignored Git state without staging the handbook.

**Tech Stack:** Markdown, Git, Windows PowerShell, Python 3.10

## Global Constraints

- The private body path is exactly `docs/private/QAgent项目维护手册.md`.
- The private body must never be staged, committed, pushed, or copied outside the QAgent task.
- Do not include real API keys, tokens, passwords, uploaded private documents, or sensitive machine configuration.
- Do not modify business source, dependencies, or tests.
- Use repository-relative paths inside the handbook.
- Describe current behavior as fact and future work as planning; do not mix the two.
- Use Chinese prose and PowerShell commands encoded as UTF-8.

---

### Task 1: Establish the private documentation boundary

**Files:**
- Modify: `.gitignore`

**Interfaces:**
- Consumes: the existing task-local ignore policy.
- Produces: a Git rule that excludes every file under `docs/private/`.

- [ ] **Step 1: Confirm the target is not currently ignored**

Run:

```powershell
git check-ignore -v -- 'docs/private/QAgent项目维护手册.md'
```

Expected: exit code 1 and no matching rule.

- [ ] **Step 2: Add the private documentation rule**

Append this section to `.gitignore`:

```gitignore

# Private local documentation
docs/private/
```

- [ ] **Step 3: Verify the rule before creating the handbook**

Run:

```powershell
git check-ignore -v --no-index -- 'docs/private/QAgent项目维护手册.md'
```

Expected: `.gitignore` reports the `docs/private/` rule.

- [ ] **Step 4: Commit only the confidentiality boundary**

Run:

```powershell
git add -- .gitignore
git diff --cached --check
git commit -m "chore: ignore private project documentation"
```

Expected: the commit contains only `.gitignore`.

---

### Task 2: Gather a verified repository snapshot

**Files:**
- Read: `AGENTS.md`
- Read: `README.md`
- Read: `task.md`
- Read: `requirements.txt`
- Read: `requirements-dev.txt`
- Read: `app.py`
- Read: `agent/*.py`
- Read: `rag/*.py`
- Read: `utils/*.py`
- Read: `tests/*.py`
- Read: `.gitignore`

**Interfaces:**
- Consumes: the current committed code and project rules.
- Produces: verified facts used in the handbook; no repository mutation.

- [ ] **Step 1: Record the code baseline**

Run:

```powershell
git rev-parse HEAD
git status --short --branch
```

Expected: one full commit hash and a clean `main` branch status.

- [ ] **Step 2: Enumerate source, tests, and dependency files**

Run:

```powershell
Get-ChildItem agent,rag,utils,tests -Recurse -File -Filter *.py |
    Sort-Object FullName |
    Select-Object FullName,Length
Get-Content -Raw -Encoding UTF8 requirements.txt
Get-Content -Raw -Encoding UTF8 requirements-dev.txt
```

Expected: all implementation and test files are visible without cache files.

- [ ] **Step 3: Read the current behavior sources completely**

Run:

```powershell
@('app.py','README.md','task.md','AGENTS.md') |
    ForEach-Object { Get-Content -Raw -Encoding UTF8 $_ }
Get-ChildItem agent,rag,utils,tests -File -Recurse -Filter *.py |
    Sort-Object FullName |
    ForEach-Object { Get-Content -Raw -Encoding UTF8 $_.FullName }
```

Expected: enough evidence to describe every module, route, data flow, test, limitation, and failure mode without guessing.

- [ ] **Step 4: Obtain fresh verification facts**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest
```

Expected: 17 tests pass without API calls.

---

### Task 3: Write the private Chinese maintenance handbook

**Files:**
- Create, ignored: `docs/private/QAgent项目维护手册.md`

**Interfaces:**
- Consumes: the verified snapshot from Task 2 and the approved design specification.
- Produces: one self-contained private handbook for the owner and future coding agents.

- [ ] **Step 1: Create the document header and fact labels**

The document must begin with:

```markdown
# QAgent 项目维护手册

> **文档属性：私有、本地、禁止提交或上传。**
>
> 本手册服务于项目所有者和后续编码 Agent。涉及当前实现的描述以指定代码基线为准；任何密钥、私人上传文档和本机敏感配置都不得写入本文件。

- 最后核对日期：2026-07-13
- 代码基线：`d9ed65333faa92add4c90e7f1854f39baaf1b175`
- 项目路径：`tasks/QAgent/`

本文使用以下标记：

- **[事实]** 当前代码已经实现并可从源码或测试验证。
- **[限制]** 当前实现中已确认的边界、风险或技术债。
- **[规划]** 尚未实现的建议，不得当作现有能力。
```

- [ ] **Step 2: Write stable sections 1–9**

Use these exact section headings and cover the listed facts:

```markdown
## 1. 文档使用规则
## 2. 项目定位、成熟度与非目标
## 3. 技术栈、依赖与目录总览
## 4. 系统架构总览
## 5. 用户请求的端到端数据流
## 6. `app.py` 与 Streamlit 会话生命周期
## 7. `agent/`：路由、Prompt、LLM、工具、工作流与记忆
## 8. `rag/`：文档摄取、分块、字符检索与上下文构建
## 9. `utils/`：计算器、文件生命周期和辅助函数
```

Requirements for these sections:

- Explain all current route names and their priority order.
- Explain every `st.session_state` key and when it is reset.
- Explain the upload temporary-file cleanup path.
- Explain the four-key workflow result contract.
- Explain how system and user messages are built.
- Explain `Memory.max_turns` as a message-count limit, not a true turn count.
- Explain fixed-size character chunking and current keyword/character scoring.
- State that `rag/index.py` is empty and vector retrieval is not implemented.
- Include compact text flows for general QA, document QA, calculator, outline, and math routes.

- [ ] **Step 3: Write stable sections 10–17**

Use these exact section headings:

```markdown
## 10. 配置、安装、启动与日常操作
## 11. 测试体系与每个测试文件的保障范围
## 12. 安全、隐私与数据处理边界
## 13. 已知限制、技术债与常见故障模式
## 14. 调试与故障排查手册
## 15. 日常维护 SOP
## 16. 推荐演进路线与阶段完成标准
## 17. 交接清单、变更触发矩阵、术语表与常用命令
```

Requirements for these sections:

- List installation commands but never include a real key.
- Explain what each of the seven test files protects and why tests remain offline.
- Distinguish security properties already present from missing production controls.
- Cover missing semantic retrieval, citations, persistence, streaming, retries, observability, quality evaluation, file limits, and multi-user isolation.
- Provide symptom → likely cause → diagnostic command → safe action troubleshooting entries.
- Provide before/change/after maintenance checklists.
- Define an evolution order: structured chunks and citations, retrieval evaluation, BM25/vector/hybrid retrieval, persistence and streaming, then optional agent tool loop.
- Give measurable completion criteria for each evolution stage.
- Include a change-trigger matrix for router, prompts, RAG, upload handling, dependencies, tests, and UI state.

- [ ] **Step 4: Add a closing maintenance record**

End with:

```markdown
## 文档维护记录

| 日期 | 代码基线 | 核对范围 | 维护人 |
|---|---|---|---|
| 2026-07-13 | `d9ed65333faa92add4c90e7f1854f39baaf1b175` | 初版：全仓库代码、测试、规则与路线图 | Codex（本地协助） |
```

Do not add names, credentials, private document contents, or machine-specific configuration.

---

### Task 4: Verify confidentiality, accuracy, and maintainability

**Files:**
- Verify, ignored: `docs/private/QAgent项目维护手册.md`
- Verify, tracked: `.gitignore`

**Interfaces:**
- Consumes: the completed handbook.
- Produces: evidence that the handbook is readable, complete, accurate, and non-public.

- [ ] **Step 1: Verify Git confidentiality**

Run:

```powershell
git check-ignore -v -- 'docs/private/QAgent项目维护手册.md'
git status --short --ignored
git ls-files -- 'docs/private/QAgent项目维护手册.md'
```

Expected: the file is ignored, appears only under an ignored directory, and `git ls-files` returns no path.

- [ ] **Step 2: Verify UTF-8 readability and required headings**

Run a PowerShell check that reads the file with `-Encoding UTF8` and fails unless all 17 numbered headings, the privacy warning, fact labels, maintenance record, change-trigger matrix, terminology, and command reference are present.

Expected: exit code 0 and a printed heading count of 17.

- [ ] **Step 3: Scan for incomplete content and credential assignments**

Search the private file for unfinished-content markers and assignment-like patterns for common secret variable names. Print only matching line numbers and pattern categories, never possible values.

Expected: no unfinished-content markers and no credential assignments.

- [ ] **Step 4: Cross-check repository facts**

Verify these handbook claims against code and tests:

- exactly seven `tests/test_*.py` files;
- 17 current tests pass;
- route names match `agent/router.py`;
- session-state keys match `app.py`;
- `rag/index.py` remains empty;
- the handbook baseline hash equals the commit captured before private-file creation.

Expected: all checks pass without modifying the handbook or repository.

- [ ] **Step 5: Verify the final tracked state**

Run:

```powershell
git status --short --branch
git diff --check
```

Expected: the private handbook is absent from tracked changes; only the expected branch-ahead state remains after the design, plan, and `.gitignore` commits.
