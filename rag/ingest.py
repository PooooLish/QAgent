from pathlib import Path
from pypdf import PdfReader


def load_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)


def load_txt_text(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8", errors="ignore")


def load_document_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return load_pdf_text(file_path)
    elif suffix in [".txt", ".md"]:
        return load_txt_text(file_path)
    else:
        raise ValueError(f"暂不支持的文件类型: {suffix}")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks