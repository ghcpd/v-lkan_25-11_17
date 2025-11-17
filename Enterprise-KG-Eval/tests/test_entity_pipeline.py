from src.enterprise_kg_eval.data_loader import Document
from src.enterprise_kg_eval.engines.regex_engine import RegexExtractionEngine
from src.enterprise_kg_eval.entity_pipeline import EntityExtractionPipeline


def test_entity_pipeline_produces_entities():
    doc = Document(
        document_id="DOC_TEST",
        text="Person: Jane Smith\nCompany: Vector Inc.\nLocation: Berlin, Germany",
    )
    schema = {
        "Person": ["name"],
        "Company": ["name"],
        "Location": ["city", "country"],
    }

    pipeline = EntityExtractionPipeline(RegexExtractionEngine())
    results = pipeline.run([doc], schema)

    assert len(results) == 1
    entity_types = {entity.entity_type for entity in results[0].predictions}
    assert {"Person", "Company", "Location"} <= entity_types
