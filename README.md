# QAgent

A lightweight General QA Agent powered by LLM, supporting document-grounded QA, multi-turn conversation, and tool-augmented reasoning.

---

## Features

- General Question Answering  
  Answer common knowledge questions.

- Document QA (RAG)  
  Upload PDF / TXT / Markdown and ask questions based on document content.

- Document Summarization  
  Automatically generate summaries for uploaded documents.

- Outline Generation  
  Generate structured outlines for a given topic.

- Tool-Augmented Reasoning  
  Includes:
  - Calculator (safe evaluation)
  - Outline generator
  - Retrieval tool

- Routing System  
  Automatically dispatch queries to:
  - General QA
  - Document QA
  - Calculator
  - Outline generator

- Multi-turn Memory  
  Maintains conversation history for contextual responses.

---

## System Architecture

User Query
   ↓
Router (intent classification)
   ↓
Tool Selection
   ↓
LLM Reasoning
   ↓
Memory Update
   ↓
Final Answer

With optional RAG pipeline:

Query → Retrieve → Context → LLM → Answer

---

## Project Structure
```
QAgent/
├── app.py # Streamlit UI
├── requirements.txt # Dependencies
├── README.md
│
├── agent/
│ ├── llm.py # OpenAI client
│ ├── memory.py # Conversation memory
│ ├── prompts.py # Prompt templates
│ ├── router.py # Query routing
│ ├── tools.py # Tools (calculator, outline, retrieval)
│ └── workflow.py # Main agent pipeline
│
├── rag/
│ ├── ingest.py # Document loading & chunking
│ ├── retrieve.py # Retrieval logic
│ └── index.py # (reserved for future vector index)
│
├── utils/
│ ├── calculator.py # Safe math evaluation
│ ├── file_utils.py # File handling
│ ├── logging_utils.py # Debug logging
│ ├── prompt_utils.py # Prompt helpers
│ └── text_utils.py # Text processing
│
├── data/
│ ├── uploads/ # Uploaded files
│ └── kb/ # (optional knowledge base)
```
---

## Installation

1. Clone repository

git clone <your-repo-url>
cd QAgent

2. Install dependencies

pip install -r requirements.txt

3. Set environment variables

Create a .env file:

OPENAI_API_KEY=your_api_key_here

---

## Usage

Start the app:

streamlit run app.py

Then open the browser and:

1. Upload a document (optional)
2. Ask questions in the chat interface

---

## Example Queries

General QA:
- What is machine learning?

Document QA:
- What is the main idea of this paper?

Summarization:
- Summarize this document

Outline:
- Generate an outline for deep learning

Calculator:
- Calculate 2^10 + 24

---

## Future Improvements

- Vector database (FAISS / Chroma)
- Embedding-based retrieval
- Web search integration
- Code execution tool
- Multi-modal support

---

## License

MIT License