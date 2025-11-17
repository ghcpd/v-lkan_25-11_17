from enterprise_kg_eval.engines.regex_engine import RegexEngine
from pathlib import Path


def test_regex_engine_extracts_person_company():
    base = Path(__file__).resolve().parents[2]
    text = "John Doe, age 32, works at OpenAI as a Researcher."
    engine = RegexEngine()
    ents = engine.extract_entities(text, {})
    types = set([e['type'] for e in ents])
    assert 'Person' in types
    assert 'Company' in types or any('OpenAI' in e['text'] for e in ents)
    rels = engine.extract_relations(text, ents, {})
    assert any(r['type'] == 'works_at' for r in rels)
