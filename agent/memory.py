class Memory:
    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self.messages = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.max_turns:]

    def get_history_text(self) -> str:
        return "\n".join(
            [f'{m["role"]}: {m["content"]}' for m in self.messages]
        )