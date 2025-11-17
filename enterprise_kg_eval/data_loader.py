from pathlib import Path
from typing import List


class DataLoader:
    """Loads documents from a plain text file. Each line is treated as a separate document for simplicity."""

    def __init__(self, documents_path: str):
        self.path = Path(documents_path)

    def load(self) -> List[str]:
        if not self.path.exists():
            raise FileNotFoundError(f"Documents file not found: {self.path}")
        with self.path.open("r", encoding="utf-8") as fh:
            # Normalize whitespace and return non-empty lines
            lines = [l.strip() for l in fh.read().splitlines()]
            return [l for l in lines if l]
