# QAgent task

## Status

Work in progress. The repository contains a Streamlit QA prototype with general QA, document ingestion, keyword retrieval, calculation, outline generation, and conversation memory.

## Current objective

Establish a maintainable engineering baseline before repairing application behavior.

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
