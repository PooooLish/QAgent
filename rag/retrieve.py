def retrieve_chunks(query: str, chunks: list[str], top_k: int = 4) -> list[str]:
    query = query.strip().lower()
    if not query or not chunks:
        return []

    scored = []
    is_chinese = any('\u4e00' <= ch <= '\u9fff' for ch in query)

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0

        if query in chunk_lower:
            score += 20

        if is_chinese:
            for ch in query:
                if ch.strip() and ch in chunk_lower:
                    score += 1
        else:
            for term in query.split():
                if term in chunk_lower:
                    score += chunk_lower.count(term) * 2

        score -= len(chunk) * 0.0005
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored[:top_k] if score > 0]