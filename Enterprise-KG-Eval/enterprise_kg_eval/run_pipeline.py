import argparse
from pathlib import Path
from .config import load_config
from .data_loader import load_documents
from .engines import RegexEngine, StubLLMEngine
from .entity_pipeline import EntityPipeline
from .relation_pipeline import RelationPipeline
from .writer import write_entities, write_relations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--docs', default='documents.txt')
    parser.add_argument('--entities', default='entities.json')
    parser.add_argument('--relations', default='relations.json')
    parser.add_argument('--engine', default='regex', choices=['regex', 'llm'])
    parser.add_argument('--out-dir', default='output')
    args = parser.parse_args()

    docs = load_documents(args.docs)
    entity_defs = load_config(args.entities)
    rel_defs = load_config(args.relations)

    engine = RegexEngine() if args.engine == 'regex' else StubLLMEngine()

    entity_pipeline = EntityPipeline(engine)
    relation_pipeline = RelationPipeline(engine)

    ent_results = entity_pipeline.run(docs, entity_defs)
    rel_results = relation_pipeline.run(docs, rel_defs)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_entities(out_dir / 'entities_output.json', ent_results)
    write_relations(out_dir / 'relations_output.json', rel_results)

    print(f"Wrote entities to {out_dir / 'entities_output.json'}")
    print(f"Wrote relations to {out_dir / 'relations_output.json'}")


if __name__ == '__main__':
    main()
