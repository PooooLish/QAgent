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
