from pathlib import Path


def get_file_extension(file_name: str) -> str:
    return Path(file_name).suffix.lower()


def save_temp_file(uploaded_file) -> str:
    import tempfile

    suffix = get_file_extension(uploaded_file.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)