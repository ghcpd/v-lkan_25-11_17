import json
from pathlib import Path
from typing import List, Dict, Any
from .schema.output_schema import EntityModel, RelationModel


class OutputWriter:
    @staticmethod
    def write_json(items: List[Dict[str, Any]], path: str):
        p = Path(path)
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        # validate and write
        if len(items) > 0 and isinstance(items[0], dict):
            # determine whether we're writing Entities or Relations by key presence
            try:
                if 'source' in items[0] and 'text' in items[0]:
                    content = [EntityModel(**it).dict() for it in items]
                elif 'source_context' in items[0]:
                    content = [RelationModel(**it).dict() for it in items]
                else:
                    content = items
                with p.open('w', encoding='utf-8') as fh:
                    json.dump(content, fh, indent=2)
                return
            except Exception:
                # if validation fails, fall back to raw dump
                pass
        # fallback write raw json
        with p.open('w', encoding='utf-8') as fh:
            json.dump(items, fh, indent=2)
