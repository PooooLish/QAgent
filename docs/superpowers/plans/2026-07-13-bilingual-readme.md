# QAgent Bilingual README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the inaccurate Agent-oriented README with aligned English and Simplified Chinese documentation that describes QAgent as the lightweight routed Chatbot it currently is.

**Architecture:** Keep `README.md` as the English GitHub entry point and add `README.zh-CN.md` as a complete Chinese counterpart. Both files use the same section order, commands, route table, architecture, limitations, and roadmap, with language links at the top.

**Tech Stack:** Markdown, Git, Windows PowerShell, pytest

## Global Constraints

- Do not modify application source, tests, dependencies, or the private handbook.
- Describe only behavior verified in the current codebase.
- Use “Chatbot prototype” for the current system and reserve “Agent” for future work.
- State that routing is deterministic and keyword-based.
- State that retrieval is character/keyword matching, not semantic vector retrieval.
- Keep route names, file paths, commands, dependency names, and test counts identical across both languages.
- Do not include real credentials, private paths, or private handbook content.

---

### Task 1: Rewrite the English README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: current `app.py`, `agent/`, `rag/`, `utils/`, `tests/`, `requirements*.txt`, and the approved design.
- Produces: the default English project entry point.

- [ ] **Step 1: Replace the title block and project positioning**

The file begins with:

```markdown
# QAgent

[English](README.md) | [简体中文](README.zh-CN.md)

QAgent is a lightweight Chinese-oriented Chatbot prototype powered by an LLM. It combines deterministic intent routing, simple tools, short in-memory conversation history, and basic document-grounded question answering.

> QAgent is not yet an autonomous Agent. The current program executes one predefined route per request; it does not let the model plan multiple steps, choose arbitrary tools, pause for approval, or resume long-running tasks.
```

- [ ] **Step 2: Write the 15 aligned English sections**

Use these exact headings:

```markdown
## Project Status
## Current Capabilities
## Why This Is Not Yet an Agent
## Architecture
## Current Router Rules
## Current RAG Pipeline
## Project Structure
## Installation
## Configuration
## Usage and Example Queries
## Tests
## Current Limitations
## Recommended Evolution Path
## Security and Privacy
## License
```

Required factual content:

- describe the five routes and their exact priority;
- describe the four-key workflow result contract;
- show `file → extract → fixed-size chunks → lexical scoring → context → LLM`;
- state chunk size 800 and overlap 120 in the UI;
- state that `Memory(max_turns=8)` retains eight messages, not eight full turns;
- list PDF/TXT/Markdown support;
- state that `rag/index.py` is empty;
- list all seven test files and 17 offline tests;
- give `python -m pip install -r requirements-dev.txt`, `streamlit run app.py`, and `python -m pytest` commands;
- list missing vector retrieval, citations, persistence, streaming, observability, quality evaluation, Agent loop, production file controls, and multi-user isolation;
- order the roadmap as structured chunks/citations → evaluation → BM25/vector/hybrid retrieval → persistence/streaming → optional Agent loop.

- [ ] **Step 3: Review English wording against source**

Run searches in `README.md` for `autonomous`, `keyword`, `17`, `rag/index.py`, `Memory(max_turns=8)`, and every route name.

Expected: every factual boundary is present and no implemented feature is described as autonomous planning.

---

### Task 2: Create the aligned Chinese README

**Files:**
- Create: `README.zh-CN.md`

**Interfaces:**
- Consumes: the completed English README and the same verified source facts.
- Produces: a complete Simplified Chinese counterpart.

- [ ] **Step 1: Create the Chinese title block**

The file begins with:

```markdown
# QAgent

[English](README.md) | [简体中文](README.zh-CN.md)

QAgent 是一个面向中文使用场景的轻量 Chatbot 原型。它结合了确定性的意图路由、简单工具、内存内短期对话历史和基础文档问答。

> QAgent 目前还不是自主 Agent。每次请求只执行一个预定义分支；模型不会自主规划多个步骤、任意选择工具、等待人工审批或恢复长时间任务。
```

- [ ] **Step 2: Write the aligned Chinese sections**

Use these exact headings in the same order as English:

```markdown
## 项目状态
## 当前能力
## 为什么它还不是 Agent
## 系统架构
## 当前 Router 规则
## 当前 RAG 流程
## 项目结构
## 安装
## 配置
## 使用方式与示例问题
## 测试
## 当前限制
## 推荐演进路线
## 安全与隐私
## License
```

Translate the English facts faithfully. Do not shorten the Chinese version or introduce capabilities absent from English.

- [ ] **Step 3: Verify language links and aligned technical facts**

Check that both files contain the same route names, commands, file paths, numeric values (`800`, `120`, `8`, `7`, `17`), and language links.

Expected: technical tokens and numbers match exactly; prose differs only by language.

---

### Task 3: Verify and commit the bilingual README

**Files:**
- Verify: `README.md`
- Verify: `README.zh-CN.md`

**Interfaces:**
- Consumes: both completed README files.
- Produces: verified, committed bilingual documentation without source changes.

- [ ] **Step 1: Check UTF-8, headings, placeholders, and credentials**

Read both files with PowerShell `-Encoding UTF8`. Verify each has 15 `##` headings, contains the language links, and has no unfinished-content marker or assignment-like secret pattern.

Expected: both checks pass without printing possible secret values.

- [ ] **Step 2: Verify technical parity**

For both files, assert the presence of:

```text
calculator
math
outline
document_qa
general_qa
chunk_size=800
overlap=120
Memory(max_turns=8)
rag/index.py
requirements-dev.txt
17
```

Expected: all tokens are present in both files.

- [ ] **Step 3: Run repository verification**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest
git diff --check
git status --short
```

Expected: 17 tests pass; only `README.md` and `README.zh-CN.md` are changed.

- [ ] **Step 4: Commit the bilingual README**

Run:

```powershell
git add -- README.md README.zh-CN.md
git commit -m "docs: clarify chatbot scope in bilingual readme"
```

Expected: one documentation-only commit containing exactly the two README files.
