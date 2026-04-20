from agent.llm import LLMClient
from agent.router import route_query
from agent.tools import calculator, generate_outline, build_document_context
from agent.prompts import (
    SYSTEM_PROMPT,
    build_document_prompt,
    build_general_prompt,
    build_tool_prompt,
)


class GeneralQAAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = LLMClient(model=model)

    def run(self, query: str, chunks: list[str], memory) -> dict:
        history_text = memory.get_history_text()
        route = route_query(query, has_document=bool(chunks))

        if route == "document_qa":
            context, retrieval_mode, retrieved_chunks = build_document_context(query, chunks)
            prompt = build_document_prompt(query, context, history_text)
            answer = self.llm.generate(prompt, SYSTEM_PROMPT)

            return {
                "route": route,
                "answer": answer,
                "retrieval_mode": retrieval_mode,
                "retrieved_chunks": retrieved_chunks,
            }

        elif route == "calculator":
            result = calculator(query)
            prompt = build_tool_prompt(query, result, history_text)
            answer = self.llm.generate(prompt, SYSTEM_PROMPT)

            return {
                "route": route,
                "answer": answer,
                "retrieval_mode": "tool",
                "retrieved_chunks": [],
            }

        elif route == "outline":
            result = generate_outline(query)
            prompt = build_tool_prompt(query, result, history_text)
            answer = self.llm.generate(prompt, SYSTEM_PROMPT)

            return {
                "route": route,
                "answer": answer,
                "retrieval_mode": "tool",
                "retrieved_chunks": [],
            }

        elif route == "math":
            prompt = f"""
        请详细、清晰地推导并解释以下数学问题：

        {query}

        要求：
        - 给出步骤
        - 给出公式
        - 用自然语言解释
        """
            answer = self.llm.generate(prompt, SYSTEM_PROMPT)

        else:
            prompt = build_general_prompt(query, history_text)
            answer = self.llm.generate(prompt, SYSTEM_PROMPT)

            return {
                "route": route,
                "answer": answer,
                "retrieval_mode": "none",
                "retrieved_chunks": [],
            }