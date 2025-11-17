import json
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2] / 'v-lkan_25-11_17'


def load_config(filename: str):
    path = Path(filename)
    if not path.exists():
        # fallback to repo root data
        alt = DEFAULT_ROOT / Path(filename).name
        path = alt if alt.exists() else path
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
