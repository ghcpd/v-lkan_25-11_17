from pathlib import Path
from enterprise_kg_eval.pipelines.entity_extractor import EntityExtractorPipeline
from enterprise_kg_eval.pipelines.relation_extractor import RelationExtractorPipeline


def test_e2e_regex_pipeline(tmp_path):
    base = Path(__file__).resolve().parents[2]
    documents = str(base / 'documents.txt')
    entities_config = str(base / 'entities.json')
    relations_config = str(base / 'relations.json')

    # outputs in tmp_path
    entity_out = tmp_path / 'entities_output.json'
    relation_out = tmp_path / 'relations_output.json'

    epipe = EntityExtractorPipeline(entities_config, documents, str(entity_out), engine='regex')
    entities = epipe.run()
    assert isinstance(entities, list)
    assert len(entities) > 0

    rpipe = RelationExtractorPipeline(relations_config, documents, entities, str(relation_out), engine='regex')
    relations = rpipe.run()
    assert isinstance(relations, list)
    # Expect some works_at relations to be found
    assert any(r['type'] == 'works_at' for r in relations)
