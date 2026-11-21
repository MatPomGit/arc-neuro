"""Generate a deliberately minimal public Pages index from explicit opt-in entries."""
from __future__ import annotations
import html
import json
import re
import sys
from pathlib import Path
from validate_repository import safe_public_page_url
from site_branding import approved_logo
from public_approvals import load_publication_approvals, is_approved_project, strict_json_loads


def safe_text(text:str)->str:
    return re.sub(r"[\[\]<>|\n\r]", " ", text).strip()


def render(root:Path)->str:
    source=strict_json_loads((root/"portfolio/projects.json").read_text(encoding="utf-8"))
    if not isinstance(source, dict) or not isinstance(source.get("projects"), list):
        raise ValueError("portfolio/projects.json requires an object with projects array")
    projects=source["projects"]
    approvals=load_publication_approvals(root)
    policy_file=root/"config/pages-policy.json"
    policy=(json.loads(policy_file.read_text(encoding="utf-8")) if policy_file.is_file()
            else {"public_files": [], "approved_image_sha256": {}})
    public=[]
    for p in projects:
        if not isinstance(p, dict):
            raise ValueError("portfolio/projects.json contains a non-object project")
        if p.get("visibility")!="public" or p.get("public_listing") is not True:
            continue
        url=p.get("pages_url")
        if not safe_public_page_url(url) or not is_approved_project(p, approvals):
            continue
        name=safe_text(str(p.get("title","Projekt")))
        ident=p.get("id")
        logo=None
        if isinstance(ident,str) and re.fullmatch(r"[a-z][a-z0-9-]{2,63}",ident):
            logo=approved_logo(root,policy,"assets/projects/"+ident)
        public.append((name,url,logo))
    lines=["# Publiczne projekty", "", "Ten katalog obejmuje wyłącznie projekty zatwierdzone do publikacji przez właściciela.",""]
    if not public:
        lines += ["Brak zatwierdzonych wpisów publicznych.",""]
    else:
        for title,url,logo in sorted(public):
            if logo:
                alt=html.escape("Logo projektu "+title,quote=True)
                lines.append(f'- <img src="{logo}" alt="{alt}" width="48" height="48" loading="lazy"> [{title}]({url})')
            else:
                lines.append(f"- [{title}]({url})")
        lines.append("")
    lines += ["Informacje o badaniach i wynikach znajdują się w kanonicznych repozytoriach projektów. Nie publikuje się tutaj danych uczestników.",""]
    return "\n".join(lines)


def main(argv:list[str]|None=None)->int:
    root=Path(__file__).resolve().parents[1]
    path=root/"pages/projects.md"
    try:
        rendered=render(root)
    except (OSError, ValueError) as exc:
        print(f"FAIL: invalid project catalog source ({type(exc).__name__})", file=sys.stderr)
        return 1
    path.write_text(rendered,encoding="utf-8")
    print("Public project catalog generated; unapproved entries excluded")
    return 0

if __name__=="__main__": sys.exit(main())
