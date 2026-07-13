from collections.abc import Callable
from pathlib import Path

from rag.ingest import load_document_text


def get_file_extension(file_name: str) -> str:
    return Path(file_name).suffix.lower()


def save_temp_file(uploaded_file) -> str:
    import tempfile

    suffix = get_file_extension(uploaded_file.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def load_uploaded_document(
    uploaded_file,
    loader: Callable[[str], str] = load_document_text,
) -> str:
    temp_path = Path(save_temp_file(uploaded_file))
    try:
        return loader(str(temp_path))
    finally:
        temp_path.unlink(missing_ok=True)


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
