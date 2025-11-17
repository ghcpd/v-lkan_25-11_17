from enterprise_kg_eval.engines import RegexEngine, StubLLMEngine
from enterprise_kg_eval.entity_pipeline import EntityPipeline
from enterprise_kg_eval.relation_pipeline import RelationPipeline
from enterprise_kg_eval.writer import write_entities, write_relations
import json
from pathlib import Path


def test_regex_engine_entities_and_relations(tmp_path):
    engine = RegexEngine()
    entity_defs = {'ORG': {'pattern': '\\b[A-Z]{2,}\\b'}}
    rel_defs = {'WORKS_FOR': {'keywords': ['works at']}}
    texts = ['ACME Corp works at AMAZON.']
    ep = EntityPipeline(engine)
    rp = RelationPipeline(engine)
    ents = ep.run(texts, entity_defs)
    rels = rp.run(texts, rel_defs)
    assert isinstance(ents[0]['entities'], list)
    assert isinstance(rels[0]['relations'], list)

    out_e = tmp_path / 'e.json'
    out_r = tmp_path / 'r.json'
    write_entities(out_e, ents)
    write_relations(out_r, rels)
    assert out_e.exists()
    assert out_r.exists()


def test_stub_engine_matches_examples():
    engine = StubLLMEngine()
    entity_defs = {'PRODUCT': {'examples': ['AcmeX']}}
    rel_defs = {'MAKES': {'examples': ['made by Acme']}}
    texts = ['The product AcmeX is made by Acme.']
    ep = EntityPipeline(engine)
    rp = RelationPipeline(engine)
    ents = ep.run(texts, entity_defs)
    rels = rp.run(texts, rel_defs)
    assert any(e['type']=='PRODUCT' for e in ents[0]['entities'])
    assert any(r['type']=='MAKES' for r in rels[0]['relations'])
