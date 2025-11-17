import subprocess
import json
import sys
import os
from pathlib import Path


def test_run_pipeline_and_output():
    cwd = os.path.join(os.getcwd(), 'Enterprise-KG-Eval')
    env = os.environ.copy()
    env['PYTHONPATH'] = cwd
    subprocess.check_call([sys.executable, '-m', 'enterprise_kg_eval.run_pipeline'], env=env, cwd=cwd)
    out_dir = Path('Enterprise-KG-Eval') / 'output'
    assert (out_dir / 'entities_output.json').exists()
    assert (out_dir / 'relations_output.json').exists()
    # check minimal validity
    data = json.loads((out_dir / 'entities_output.json').read_text())
    assert 'entities' in data
    data2 = json.loads((out_dir / 'relations_output.json').read_text())
    assert 'relations' in data2
