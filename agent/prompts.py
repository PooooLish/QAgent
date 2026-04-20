SYSTEM_PROMPT = """
You are a helpful QA agent.
You can answer general questions, summarize documents, generate outlines, and explain tool results.
Please answer in Chinese.
Do not make up information when context is insufficient.
""".strip()


def build_document_prompt(query: str, context: str, history_text: str = "") -> str:
    return f"""
Recent conversation:
{history_text}

Document context:
{context}

Question:
{query}

Please answer only based on the document context when possible.
""".strip()


def build_general_prompt(query: str, history_text: str = "") -> str:
    return f"""
Recent conversation:
{history_text}

Question:
{query}
""".strip()


def build_tool_prompt(query: str, tool_result: str, history_text: str = "") -> str:
    return f"""
Recent conversation:
{history_text}

User question:
{query}

Tool result:
{tool_result}

Please provide a natural and helpful answer in Chinese.
""".strip()