# QAgent

[English](README.md) | [简体中文](README.zh-CN.md)

QAgent is a lightweight Chinese-oriented Chatbot prototype powered by an LLM. It combines deterministic intent routing, simple tools, short in-memory conversation history, and basic document-grounded question answering.

> QAgent is not yet an autonomous Agent. The current program executes one predefined route per request; it does not let the model plan multiple steps, choose arbitrary tools, pause for approval, or resume long-running tasks.

## Project Status

QAgent is a work-in-progress learning and experimentation project. It is suitable for local demonstrations and architecture experiments, but it is not a production-ready, multi-user service.

The name **QAgent** is retained as a possible future direction. It does not claim that the current implementation already has autonomous Agent capabilities.

## Current Capabilities

- General Chinese-oriented LLM question answering.
- PDF, TXT, and Markdown document upload and text extraction.
- Basic document QA and document summarization.
- Safe arithmetic through a restricted Python AST evaluator.
- LLM-based explanations for derivatives, integrals, and limits.
- Fixed-template outline generation.
- Short in-memory conversation history.
- Streamlit chat interface with route and retrieval details.

## Why This Is Not Yet an Agent

The current program is a tool-augmented Chatbot with deterministic routing. Application code—not the model—selects one branch for each request.

It does not currently provide:

- model-driven tool selection;
- multi-step planning or a tool execution loop;
- dynamic replanning after observing tool results;
- human approval for high-risk actions;
- persistent task state, pause/resume, or failure recovery;
- execution budgets, maximum steps, or tool permissions.

## Architecture

```text
User input
  ↓
Streamlit UI and session state
  ↓
Keyword-based Router
  ↓
One predefined workflow branch
  ├─ calculator
  ├─ math explanation
  ├─ outline generator
  ├─ document QA
  └─ general QA
  ↓
LLM response
  ↓
Memory and UI update
```

Every workflow branch returns the same result contract:

```python
{
    "route": str,
    "answer": str,
    "retrieval_mode": str,
    "retrieved_chunks": list[str],
}
```

## Current Router Rules

Rules are evaluated in this exact order:

| Priority | Condition | Route |
|---:|---|---|
| 1 | Contains `积分`, `导数`, or `极限` | `math` |
| 2 | Becomes a valid arithmetic expression after optional calculation wording is removed | `calculator` |
| 3 | A document is loaded and the query contains summary, explicit document, or document-reference terms | `document_qa` |
| 4 | Contains `提纲` or `outline` | `outline` |
| 5 | Everything else | `general_qa` |

The calculator rule requires both a number and an arithmetic operator. A standalone `/` or `-`, URLs, dates such as `2026-07-13`, version numbers, and prose containing those characters do not trigger it. This design is fast, transparent, and easy to test, but it remains sensitive to missing keywords, ambiguous queries, and paraphrases.

## Current RAG Pipeline

```text
PDF/TXT/Markdown
  → text extraction
  → fixed-size character chunks
  → character/keyword scoring
  → context truncation
  → LLM answer
```

The Streamlit upload flow calls `chunk_text(text, chunk_size=800, overlap=120)`. Retrieval is lexical: it scores exact query matches, Chinese character overlap, or whitespace-separated English terms. It is not embedding-based semantic retrieval.

Current RAG limitations:

- chunks are plain strings without source, page, section, or stable IDs;
- PDF page metadata is not retained;
- answers do not include citations;
- there is no BM25, embedding model, vector database, hybrid retrieval, or reranker;
- `rag/index.py` is currently empty;
- retrieval quality is not yet measured with an evaluation dataset.

## Project Structure

```text
QAgent/
├── app.py                  # Streamlit UI and session orchestration
├── agent/
│   ├── llm.py              # OpenAI client and message construction
│   ├── memory.py           # Short in-memory message history
│   ├── prompts.py          # Prompt builders
│   ├── router.py           # Deterministic intent routing
│   ├── tools.py            # Calculator, outline, and RAG context tools
│   └── workflow.py         # Main routed workflow
├── rag/
│   ├── ingest.py           # Document extraction and chunking
│   ├── retrieve.py         # Lexical retrieval
│   └── index.py            # Empty placeholder; no vector index yet
├── utils/                  # Calculator, temporary files, and helpers
├── tests/                  # Offline unit and regression tests
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Runtime dependencies plus pytest
└── pytest.ini              # Test discovery configuration
```

## Installation

Python 3.10 or newer is recommended.

```powershell
git clone https://github.com/PooooLish/QAgent.git
cd QAgent
python -m pip install -r requirements-dev.txt
```

For runtime-only installation, use `requirements.txt` instead.

## Configuration

Set `OPENAI_API_KEY` in the current process environment before starting the application. Never commit the real value to Git.

The current default model is `gpt-4o-mini`, configured when `GeneralQAAgent` is created in `app.py`.

`Memory(max_turns=8)` retains the last eight messages, not eight complete user/assistant turns. Conversation state is not persisted across process restarts.

## Usage and Example Queries

Start the application:

```powershell
streamlit run app.py
```

Examples:

- General QA: `什么是机器学习？`
- Document QA: upload a file, then ask `这个文档的主要结论是什么？`
- Summary: `总结这份文档的主要内容`
- Outline: `生成一个深度学习学习提纲`
- Calculator: `计算 2^10 + 24`
- Math: `解释 x² 的导数`

## Tests

The repository contains 7 test files and 17 offline tests. They cover routing, calculator safety, chunking, lexical retrieval, LLM message construction, math workflow results, and temporary-file cleanup.

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest
```

The tests do not make real OpenAI API calls or start a Streamlit browser. They verify implemented behavior, not answer or retrieval quality.

## Current Limitations

- Keyword routing can misclassify paraphrases and mixed-intent queries.
- Document questions may miss RAG unless they include recognized document keywords.
- Retrieval is lexical rather than semantic.
- Responses have no source citations or grounding score.
- Conversation and document state are memory-only.
- There is no streaming, retry, timeout, cancellation, token accounting, or observability.
- Uploaded files have no production-grade size, page-count, MIME, or parsing-time limits.
- There is no user authentication, authorization, or multi-user data isolation.
- There is no real Agent loop or autonomous multi-tool execution.

## Recommended Evolution Path

1. Introduce structured chunks with source, page, section, and stable IDs.
2. Add grounded citations and explicit insufficient-evidence responses.
3. Build a small retrieval evaluation dataset and record Recall@k and MRR.
4. Compare the current lexical baseline with BM25, vector, and hybrid retrieval.
5. Add persistence, streaming, timeouts, retries, and basic observability.
6. Add a controlled Agent tool loop only when real multi-step use cases require it.

## Security and Privacy

- Do not commit API keys, `.env` files, uploaded documents, logs, caches, or private local documentation.
- Treat uploaded document text as untrusted input.
- Do not execute model-generated code directly.
- Keep tests offline and use non-private fixtures.
- Add file limits, user isolation, tool permissions, and audit logging before production use.

## License

This repository currently does not include a `LICENSE` file. Do not assume that the code is licensed under MIT or another open-source license until the project owner adds an explicit license.
