import subprocess
import sys
from pathlib import Path


def test_structural_runner_imports_when_executed_as_script():
    repo = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            str(repo / "empirical/run_fournations_structural_outputs.py"),
            "--help",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
