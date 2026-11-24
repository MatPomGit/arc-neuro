"""Generate transparent aggregate CSV and SVG reports for P06 analyses."""
from __future__ import annotations
import csv
import html
from pathlib import Path

LABELS = {"H1":"Trafność po interwencji","H2":"Trafność po tygodniu",
          "H3":"Wynik Briera","H4":"Jakość uzasadnienia"}


def write_report(results, output_dir, *, source="SYNTHETIC"):
    """Write only aggregate estimates. SOURCE is explicit, no silent empirical claim."""
    if source not in ("SYNTHETIC","PILOT","MAIN"):
        raise ValueError("Invalid source label")
    if set(results)!=set(LABELS):
        raise ValueError("All four hypotheses required")
    output=Path(output_dir)
    output.mkdir(parents=True,exist_ok=True)
    fields=["source","hypothesis","unit","estimate","se","ci_low","ci_high","p","p_adjusted","n_randomized","n_used","reference"]
    with (output/"effects.csv").open("w",encoding="utf-8",newline="") as file:
        writer=csv.DictWriter(file,fieldnames=fields)
        writer.writeheader()
        for h in LABELS:
            r=results[h]
            writer.writerow({**{k:r[k] for k in fields if k not in ("source","ci_low","ci_high")},
                             "source":source,"ci_low":r["ci"][0],"ci_high":r["ci"][1]})
    # Separate panels/axes for distinct units; never compare raw lengths across them.
    groups=[("Punkty procentowe",("H1","H2")),("Wynik Briera",("H3",)),("Punkty rubryki 0–2",("H4",))]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="490" viewBox="0 0 860 490">',
         '<rect width="860" height="490" fill="white"/>',
         '<g font-family="sans-serif" fill="#111827" font-size="14">',
         f'<text x="25" y="25" font-size="16">MSC-CR-P06 · {html.escape(source)} · ANCOVA, 95% CI</text>']
    for k,(unit,hs) in enumerate(groups):
        top=48+k*143
        bounds=[0.]+[v for h in hs for v in results[h]["ci"]]
        lo,hi=min(bounds),max(bounds)
        pad=max((hi-lo)*.10,.001)
        lo,hi=lo-pad,hi+pad
        def xpos(v):
            return 305+520*(v-lo)/(hi-lo)
        axis_y=top+111
        svg.append(f'<text x="305" y="{top}">{html.escape(unit)}</text>')
        svg.append(f'<line x1="{xpos(0):.2f}" y1="{top+12}" x2="{xpos(0):.2f}" y2="{axis_y}" stroke="#64748b" stroke-dasharray="4 4"/>')
        for i,h in enumerate(hs):
            y=top+35+i*34
            r=results[h]; l,u=r["ci"]
            svg.append(f'<text x="25" y="{y+5}">{html.escape(h+" "+LABELS[h])}</text>')
            svg.append(f'<line x1="{xpos(l):.2f}" y1="{y}" x2="{xpos(u):.2f}" y2="{y}" stroke="#111827" stroke-width="2"/>')
            svg.append(f'<circle cx="{xpos(r["estimate"]):.2f}" cy="{y}" r="4" fill="#111827"/>')
        svg.append(f'<line x1="305" y1="{axis_y}" x2="825" y2="{axis_y}" stroke="#111827"/>')
        for i in range(5):
            v=lo+(hi-lo)*i/4; x=xpos(v)
            svg.append(f'<line x1="{x:.2f}" y1="{axis_y}" x2="{x:.2f}" y2="{axis_y+5}" stroke="#111827"/>')
            svg.append(f'<text x="{x:.2f}" y="{axis_y+19}" text-anchor="middle">{v:.3g}</text>')
    svg.append('</g></svg>')
    (output/"effects.svg").write_text("\n".join(svg),encoding="utf-8")
