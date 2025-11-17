"""High-level orchestration for the Enterprise-KG-Eval pipelines."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

from .config_loader import ExtractionConfig, load_config
from .data_loader import DocumentLoader
from .engine_factory import get_engine
from .entity_pipeline import EntityExtractionPipeline
from .output_writer import UnifiedOutputWriter
from .relation_pipeline import RelationExtractionPipeline


class PipelineRunner:
    """Runs entity and relation pipelines end-to-end."""

    def __init__(
        self,
        *,
        project_name: str,
        documents_path: Path | str,
        entity_config_path: Path | str,
        relation_config_path: Path | str,
        output_dir: Path | str = "output",
        engine_name: str = "regex",
    ) -> None:
        self.project_name = project_name
        self.documents_path = Path(documents_path)
        self.entity_config_path = Path(entity_config_path)
        self.relation_config_path = Path(relation_config_path)
        self.output_dir = Path(output_dir)
        self.engine_name = engine_name
        self.config: Optional[ExtractionConfig] = None

    def load_config(self) -> ExtractionConfig:
        if self.config is None:
            self.config = load_config(self.entity_config_path, self.relation_config_path)
        return self.config

    def run(self) -> Tuple[Path, Path]:
        """Execute entity and relation extraction and persist outputs."""
        config = self.load_config()
        documents = DocumentLoader(self.documents_path).load()
        engine = get_engine(self.engine_name)

        entity_pipeline = EntityExtractionPipeline(engine)
        entity_results = entity_pipeline.run(documents, config.entities)

        relation_pipeline = RelationExtractionPipeline(engine)
        relation_results = relation_pipeline.run(entity_results, config.relations)

        writer = UnifiedOutputWriter(
            self.output_dir / "entities_output.json",
            self.output_dir / "relations_output.json",
        )
        entity_path = writer.write_entities(self.project_name, entity_results)
        relation_path = writer.write_relations(self.project_name, relation_results)
        return entity_path, relation_path

