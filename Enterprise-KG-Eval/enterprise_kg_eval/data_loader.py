from pathlib import Path
from typing import List


def load_documents(path: str) -> List[str]:
    p = Path(path)
    if not p.exists():
        p = Path(__file__).resolve().parents[1] / '..' / 'v-lkan_25-11_17' / 'documents.txt'
    if not p.exists():
        raise FileNotFoundError(f"documents.txt not found at {path}")
    with open(p, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
