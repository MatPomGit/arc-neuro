"""Reproducible scenario matrix and aggregate CSV/SVG for synthetic P06 simulations."""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import itertools
import json
import math
from pathlib import Path
from sensitivity import simulate, MECHANISMS

METHODS=("full","complete_case","pmm","pmm_delta_intervention","pmm_delta_control",
         "pmm_delta10_intervention","pmm_delta10_control")
PROFILES={
    "smoke":dict(ns=(24,),effects=(0.,.08),dropouts=(.15,),repetitions=4,m=3,iterations=2),
    "screen":dict(ns=(72,),effects=(0.,.08),dropouts=(.15,.30),repetitions=50,m=10,iterations=5),
    "full":dict(ns=(72,144),effects=(0.,.08),dropouts=(.15,.30),repetitions=1000,m=50,iterations=20),
}


def scenarios(profile,seed=20261124):
    if profile not in PROFILES or type(seed) is not int:
        raise ValueError("Invalid profile or seed")
    settings=PROFILES[profile]
    result=[]
    for mechanism,n,effect,dropout in itertools.product(MECHANISMS,settings["ns"],settings["effects"],settings["dropouts"]):
        sid=f"{mechanism}-n{n}-e{round(effect*100):02d}-r{round(dropout*100):02d}"
        # Same scenario receives the same seed in different profiles.
        derived=int.from_bytes(hashlib.sha256(f"{seed}:{sid}".encode()).digest()[:8],"big")
        result.append((sid,dict(mechanism=mechanism,n_per_arm=n,effect=effect,dropout=dropout,
                                repetitions=settings["repetitions"],m=settings["m"],iterations=settings["iterations"],seed=derived)))
    return result


def run_matrix(profile,seed=20261124,selected=None,missing_scope="accuracy"):
    if profile=="full" and selected is None:
        raise ValueError("Full profile requires one explicit scenario")
    if missing_scope not in ("accuracy","session"):
        raise ValueError("Invalid missing scope")
    options=scenarios(profile,seed)
    if selected is not None and selected not in {sid for sid,_ in options}:
        raise ValueError("Unknown scenario")
    results=[]
    for sid,settings in options:
        if selected is None or sid==selected:
            results.append({"scenario":sid,**simulate(**settings,missing_scope=missing_scope)})
    return {"source":"SYNTHETIC_MONTE_CARLO_ONLY","profile":profile,
            "interpretation":"TECHNICAL_SMOKE_ONLY" if profile=="smoke" else
                             "EXPLORATORY_SCREEN_ONLY" if profile=="screen" else "MODEL_BASED_SIMULATION_ONLY",
            "master_seed":seed,"scenarios":results}


def flatten(matrix):
    rows=[]
    for scenario in matrix["scenarios"]:
        for method in METHODS:
            metrics=scenario["methods"][method]
            rows.append({"source":matrix["source"],"profile":matrix["profile"],
                         "scenario":scenario["scenario"],"method":method,
                         "truth_pp":scenario["truth_pp"],
                         "missing_fraction":scenario["realized_missing_fraction"],
                         **scenario["settings"],**{k:v for k,v in metrics.items() if k!="failure_reasons"}})
    return rows


def write_results(matrix,output_dir):
    output=Path(output_dir)
    output.mkdir(parents=True,exist_ok=True)
    rows=flatten(matrix)
    (output/"matrix.json").write_text(json.dumps(matrix,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    with (output/"matrix.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    # Two panels with independent axes, explicit null and 95% reference lines.
    plotted=[r for r in rows if r["method"] in ("full","complete_case","pmm")]
    height=100+24*len(plotted)
    bias_lim=max(1.,max((abs(r["bias"]) for r in plotted if r["bias"] is not None),default=0.))*1.15
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="{height}" viewBox="0 0 1050 {height}">',
         f'<rect width="1050" height="{height}" fill="white"/>',
         '<g font-family="sans-serif" font-size="12" fill="#172033">',
         f'<text x="15" y="22" font-size="15">P06 · SYNTHETIC · {html.escape(matrix["profile"])} · successful fits only</text>',
         '<text x="385" y="45">Bias (percentage points)</text><text x="745" y="45">95% CI coverage</text>']
    def bx(v): return 380+280*(v+bias_lim)/(2*bias_lim)
    def cx(v): return 740+280*v
    for pos in (bx(0),cx(.95)):
        svg.append(f'<line x1="{pos}" y1="52" x2="{pos}" y2="{height-30}" stroke="#64748b" stroke-dasharray="4 4"/>')
    for i,r in enumerate(plotted):
        y=65+i*24
        label=html.escape(f'{r["scenario"]} · {r["method"]} ({r["successful"]}/{r["repetitions"]})')
        svg.append(f'<text x="15" y="{y+4}">{label}</text>')
        for k,pos in (("bias",bx),("coverage",cx)):
            v=r[k]
            if v is not None:
                svg.append(f'<circle cx="{pos(v):.3f}" cy="{y}" r="4" fill="#1e3a5f"/>')
    y=height-26
    for x1,x2 in ((380,660),(740,1020)):
        svg.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#172033"/>')
    for v in (-bias_lim,0,bias_lim):
        svg.append(f'<text x="{bx(v):.2f}" y="{y+17}" text-anchor="middle">{v:.2f}</text>')
    for v in (0,.5,1):
        svg.append(f'<text x="{cx(v):.2f}" y="{y+17}" text-anchor="middle">{v:.2f}</text>')
    svg.append("</g></svg>")
    (output/"matrix.svg").write_text("\n".join(svg),encoding="utf-8")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile",choices=PROFILES,default="smoke")
    parser.add_argument("--seed",type=int,default=20261124)
    parser.add_argument("--scenario")
    parser.add_argument("--missing-scope",choices=("accuracy","session"),default="accuracy")
    parser.add_argument("--list",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.list:
        print(json.dumps(scenarios(args.profile,args.seed),indent=2))
    else:
        if not args.output:
            parser.error("--output required when executing")
        if args.profile=="full" and not args.scenario:
            parser.error("Full profile requires one explicit --scenario per invocation")
        matrix=run_matrix(args.profile,args.seed,args.scenario,args.missing_scope)
        write_results(matrix,args.output)
        print(json.dumps(matrix,allow_nan=False))
