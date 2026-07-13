import sys
import types

openai_stub = types.ModuleType("openai")
openai_stub.OpenAI = object
sys.modules.setdefault("openai", openai_stub)

from agent.llm import LLMClient


class FakeCompletions:
    def __init__(self):
        self.messages = None

    def create(self, *, model, messages):
        self.messages = messages
        message = types.SimpleNamespace(content="answer")
        choice = types.SimpleNamespace(message=message)
        return types.SimpleNamespace(choices=[choice])


def make_client():
    client = LLMClient.__new__(LLMClient)
    completions = FakeCompletions()
    client.client = types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=completions)
    )
    client.model = "test-model"
    return client, completions


def test_generate_sends_system_and_user_messages_without_duplication():
    client, completions = make_client()
    assert client.generate("question", "instructions") == "answer"
    assert completions.messages == [
        {"role": "system", "content": "instructions"},
        {"role": "user", "content": "question"},
    ]


def test_generate_omits_system_message_when_not_provided():
    client, completions = make_client()
    client.generate("question")
    assert completions.messages == [
        {"role": "user", "content": "question"},
    ]
