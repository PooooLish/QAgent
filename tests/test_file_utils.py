from pathlib import Path

import pytest

from utils.file_utils import load_uploaded_document


class FakeUpload:
    name = "notes.txt"

    def read(self):
        return b"hello"


def test_removes_temporary_file_after_successful_load():
    seen_path = None

    def loader(path):
        nonlocal seen_path
        seen_path = Path(path)
        assert seen_path.exists()
        return "loaded"

    assert load_uploaded_document(FakeUpload(), loader=loader) == "loaded"
    assert seen_path is not None
    assert not seen_path.exists()


def test_removes_temporary_file_when_loader_raises():
    seen_path = None

    def loader(path):
        nonlocal seen_path
        seen_path = Path(path)
        raise ValueError("bad document")

    with pytest.raises(ValueError, match="bad document"):
        load_uploaded_document(FakeUpload(), loader=loader)

    assert seen_path is not None
    assert not seen_path.exists()
