import argparse
from pathlib import Path
from .pipelines.entity_extractor import EntityExtractorPipeline
from .pipelines.relation_extractor import RelationExtractorPipeline


def run(entity_engine: str = 'regex', relation_engine: str = 'regex'):
    base_dir = Path(__file__).parent.parent
    entities_config = base_dir / 'entities.json'
    relations_config = base_dir / 'relations.json'
    documents = base_dir / 'documents.txt'
    output_dir = base_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    entity_output = output_dir / 'entities_output.json'
    relation_output = output_dir / 'relations_output.json'

    epipe = EntityExtractorPipeline(str(entities_config), str(documents), str(entity_output), engine=entity_engine)
    entities = epipe.run()

    rpipe = RelationExtractorPipeline(str(relations_config), str(documents), entities, str(relation_output), engine=relation_engine)
    relations = rpipe.run()

    print(f"Wrote {len(entities)} entities to {entity_output}")
    print(f"Wrote {len(relations)} relations to {relation_output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--entity-engine', default='regex')
    parser.add_argument('--relation-engine', default='regex')
    args = parser.parse_args()
    run(entity_engine=args.entity_engine, relation_engine=args.relation_engine)
