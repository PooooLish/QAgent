import os
from openai import OpenAI


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 未设置，请先配置环境变量。")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        if system_prompt:
            full_input = f"{system_prompt}\n\n{prompt}"
        else:
            full_input = prompt

        response = self.client.responses.create(
            model=self.model,
            input=full_input,
        )
        return response.output_text