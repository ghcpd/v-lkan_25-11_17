from pathlib import Path
from enterprise_kg_eval.output_writer import OutputWriter


def test_output_writer_validates(tmp_path):
    e = {
        "id": "1",
        "type": "Person",
        "text": "John Doe",
        "attributes": {"name": "John Doe", "age": 32},
        "confidence": 0.95,
        "method": "regex",
        "source": {"doc_id": 0, "text": "John Doe, age 32, works at OpenAI as a Researcher."},
    }
    p = tmp_path / 'out.json'
    OutputWriter.write_json([e], str(p))
    assert p.exists()
    content = p.read_text()
    assert 'John Doe' in content

    r = {
        "id": "2",
        "type": "works_at",
        "source": "1",
        "target": "2",
        "attributes": {},
        "confidence": 0.9,
        "method": "regex",
        "source_context": {"doc_id": 0, "text": "John Doe, age 32, works at OpenAI as a Researcher."},
    }
    p2 = tmp_path / 'out2.json'
    OutputWriter.write_json([r], str(p2))
    assert p2.exists()
    assert 'works_at' in p2.read_text()
