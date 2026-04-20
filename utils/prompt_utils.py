def build_chat_prompt(system: str, history: str, user_input: str) -> str:
    return f"""
{system}

历史对话：
{history}

用户问题：
{user_input}
""".strip()


def enforce_max_context(context: str, max_len: int = 3000) -> str:
    if len(context) > max_len:
        return context[:max_len]
    return context