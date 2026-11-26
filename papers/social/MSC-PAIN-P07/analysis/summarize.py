"""Generate the manuscript table from the versioned synthetic results."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABELS = {
    "small": "Mały",
    "moderate": "Umiarkowany",
    "large": "Duży",
    "heterogeneous": "Heterogeniczny",
}


def write_summary():
    with (ROOT / "power.csv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    lines = [
        r"\begin{table}[htbp]\centering",
        r"\caption{Syntetyczna moc dla H1. Najmniejsze $N$ w badanej siatce spełniające kryterium.}",
        r"\begin{tabular}{lrrr}\toprule",
        r"Scenariusz & $N$ & Moc & 95\% przedział MC \\ \midrule",
    ]
    for scenario, label in LABELS.items():
        eligible = [row for row in rows if row["synthetic_scenario"] == scenario and float(row["mc_low"]) >= .80]
        if not eligible:
            lines.append(f"{label} & poza siatką & & " + r"\\")
            continue
        best = min(eligible, key=lambda row: int(row["randomized_n"]))
        power, low, high = (f"{float(best[key]):.3f}".replace(".", "{,}") for key in ("power", "mc_low", "mc_high"))
        lines.append(f"{label} & {best['randomized_n']} & ${power}$ & $[{low};\\ {high}]$ " + r"\\")
    lines.append(r"\bottomrule\end{tabular}\end{table}")
    (ROOT.parent / "power-summary.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_summary()
