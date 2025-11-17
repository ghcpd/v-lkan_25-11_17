"""Load entity and relation configuration files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class ConfigLoader:
    """Loader that resolves definitions relative to a base path."""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = Path(base_path or Path.cwd())

    def _resolve(self, path: Path) -> Path:
        if path.is_absolute():
            return path
        return self.base_path / path

    def load_entity_definitions(self, path: Path) -> Dict[str, List[str]]:
        """Return entity type -> attribute name order."""
        resolved = self._resolve(path)
        with resolved.open("r", encoding="utf-8") as src:
            return json.load(src)

    def load_relation_definitions(self, path: Path) -> Dict[str, List[str]]:
        """Return relation definitions as provided by the config."""
        resolved = self._resolve(path)
        with resolved.open("r", encoding="utf-8") as src:
            return json.load(src)
