def clean_text(text: str) -> str:
    """基础清洗"""
    return text.replace("\n", " ").strip()


def truncate_text(text: str, max_len: int = 2000) -> str:
    """防止 prompt 太长"""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def split_sentences(text: str) -> list[str]:
    """简单句子切分"""
    import re
    return re.split(r"[。！？.!?]", text)