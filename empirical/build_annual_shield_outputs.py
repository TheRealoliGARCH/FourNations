from pathlib import Path

from empirical.build_shield_diagnostics import build_shield_diagnostics
from empirical.build_snp_shield_panel import build_snp_shield_panel


def build_outputs(output_dir="results"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    panel = build_snp_shield_panel()
    diagnostics = build_shield_diagnostics()
    panel.to_csv(output / "annual_snp_shield_panel.csv", index=False)
    diagnostics.to_csv(output / "annual_snp_shield_diagnostics.csv", index=False)
    return panel, diagnostics


if __name__ == "__main__":
    build_outputs()
