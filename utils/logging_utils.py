def log_step(title: str, content: str):
    print(f"\n===== {title} =====")
    print(content)


def log_route(route: str):
    print(f"[ROUTE] → {route}")


def log_chunks(chunks: list[str]):
    print(f"[RETRIEVED] {len(chunks)} chunks")