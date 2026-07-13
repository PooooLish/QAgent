import sys
import types

openai_stub = types.ModuleType("openai")
openai_stub.OpenAI = object
sys.modules.setdefault("openai", openai_stub)

from agent.workflow import GeneralQAAgent


class FakeLLM:
    def generate(self, prompt, system_prompt=None):
        return "x² 的导数是 2x"


class FakeMemory:
    def get_history_text(self):
        return ""


def test_math_route_returns_complete_result():
    agent = GeneralQAAgent.__new__(GeneralQAAgent)
    agent.llm = FakeLLM()

    result = agent.run("求 x² 的导数", [], FakeMemory())

    assert result == {
        "route": "math",
        "answer": "x² 的导数是 2x",
        "retrieval_mode": "none",
        "retrieved_chunks": [],
    }
