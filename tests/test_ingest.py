from rag.ingest import chunk_text


def test_returns_no_chunks_for_blank_text():
    assert chunk_text("   ") == []


def test_chunks_text_with_overlap():
    assert chunk_text("abcdefghij", chunk_size=4, overlap=1) == [
        "abcd",
        "defg",
        "ghij",
        "j",
    ]
