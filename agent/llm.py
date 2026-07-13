import os
from openai import OpenAI


def build_messages(
    prompt: str, system_prompt: str | None = None
) -> list[dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 未设置，请先配置环境变量。")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=build_messages(prompt, system_prompt),
        )
        return response.choices[0].message.content
