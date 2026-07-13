from rag.retrieve import retrieve_chunks


def test_returns_matching_chunk_first():
    chunks = ["bananas are yellow", "apples are red", "grapes are purple"]
    assert retrieve_chunks("apples", chunks, top_k=1) == ["apples are red"]


def test_returns_no_chunks_for_blank_query():
    assert retrieve_chunks("", ["content"]) == []
