from src.enterprise_kg_eval.config_loader import RelationSchema
from src.enterprise_kg_eval.data_loader import Document
from src.enterprise_kg_eval.engines.regex_engine import RegexExtractionEngine
from src.enterprise_kg_eval.entity_pipeline import EntityExtractionPipeline
from src.enterprise_kg_eval.relation_pipeline import RelationExtractionPipeline


def test_relation_pipeline_detects_works_at():
    document = Document(
        document_id="DOC_REL",
        text="Person: John Doe\nCompany: Apex Corporation\nJohn Doe works at Apex Corporation.",
    )
    entity_schema = {"Person": ["name"], "Company": ["name"]}
    relation_schema: RelationSchema = {"works_at": ["Person", "Company"]}

    engine = RegexExtractionEngine()
    entity_results = EntityExtractionPipeline(engine).run([document], entity_schema)
    relation_results = RelationExtractionPipeline(engine).run(entity_results, relation_schema)

    assert len(relation_results) == 1
    relations = relation_results[0].relations
    assert relations
    assert relations[0].source == "John Doe"
    assert relations[0].target == "Apex Corporation"
