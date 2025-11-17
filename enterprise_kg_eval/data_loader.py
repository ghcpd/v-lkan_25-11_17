"""Document loading utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class DocumentSegment:
    id: int
    text: str


def load_documents(path: Path) -> List[DocumentSegment]:
    """Read a text document and emit one segment per non-empty line."""
    resolved = path if path.is_absolute() else Path.cwd() / path
    if not resolved.is_file():
        raise FileNotFoundError(f"Document file missing: {resolved}")
    lines = resolved.read_text(encoding="utf-8").splitlines()
    return [
        DocumentSegment(id=index + 1, text=line.strip())
        for index, line in enumerate(lines)
        if line.strip()
    ]
