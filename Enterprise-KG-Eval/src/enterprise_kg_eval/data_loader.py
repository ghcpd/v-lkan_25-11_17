"""Utilities for loading enterprise documents from text files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass
class Document:
    """Simple document container."""

    document_id: str
    text: str


class DocumentLoader:
    """Loads enterprise documents from disk."""

    def __init__(
        self,
        file_path: Path | str,
        *,
        delimiter: str = "\n\n",
        encoding: str = "utf-8",
    ) -> None:
        self.path = Path(file_path)
        self.delimiter = delimiter
        self.encoding = encoding

    def load(self) -> List[Document]:
        """Read documents file and split into logical records."""
        if not self.path.exists():
            raise FileNotFoundError(f"Document file not found: {self.path}")

        raw_text = self.path.read_text(encoding=self.encoding)
        segments = self._split_documents(raw_text)
        return [
            Document(document_id=f"DOC_{index:04d}", text=segment.strip())
            for index, segment in enumerate(segments, start=1)
            if segment.strip()
        ]

    def iter_documents(self) -> Iterable[Document]:
        """Generator version of :meth:`load` to avoid holding all docs."""
        for document in self.load():
            yield document

    def _split_documents(self, raw_text: str) -> Sequence[str]:
        if not raw_text.strip():
            return []
        return [segment for segment in raw_text.split(self.delimiter)]

