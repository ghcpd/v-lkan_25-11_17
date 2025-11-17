from pathlib import Path

from src.enterprise_kg_eval.data_loader import DocumentLoader


def test_document_loader_splits_by_double_newline(tmp_path):
    docs = tmp_path / "docs.txt"
    docs.write_text("Doc A\n\nDoc B line1\nline2")

    loader = DocumentLoader(docs)
    documents = loader.load()

    assert len(documents) == 2
    assert documents[0].document_id == "DOC_0001"
    assert documents[1].text.endswith("line2")


def test_document_loader_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    loader = DocumentLoader(missing)
    try:
        loader.load()
    except FileNotFoundError as exc:
        assert "missing.txt" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")
