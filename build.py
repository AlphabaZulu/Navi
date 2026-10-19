#!/usr/bin/env python3
"""Build NAVI Free into a single self-contained index.html for GitHub Pages.

Edit the files in src/ (index.html, styles.css, engine.js, app.js and the
knowledge base in src/knowledge/*.json), then run:

    python3 build.py

The output is ./index.html, with the CSS, JavaScript and knowledge base
inlined. One file means the site works from GitHub Pages, from a downloaded
copy, or offline. No dependencies beyond the Python standard library.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def fail(msg):
    sys.exit(f"build.py: {msg}")


def load_knowledge():
    """Merge and validate src/knowledge/*.json into one object."""
    kdir = SRC / "knowledge"
    fw = json.loads((kdir / "frameworks.json").read_text(encoding="utf-8"))
    ob = json.loads((kdir / "obligations.json").read_text(encoding="utf-8"))
    ct = json.loads((kdir / "controls.json").read_text(encoding="utf-8"))
    frameworks, obligations, controls = fw["frameworks"], ob["obligations"], ct["controls"]
    fw_ids = {f["id"] for f in frameworks}
    ct_ids = {c["id"] for c in controls}
    for f in frameworks:
        for key in ("id", "name", "short", "jurisdiction", "type", "typeLabel", "status", "source", "verified", "verification"):
            if not f.get(key):
                fail(f"framework {f.get('id')!r} is missing {key!r}")
    seen = set()
    for o in obligations:
        if o["id"] in seen:
            fail(f"duplicate obligation id {o['id']!r}")
        seen.add(o["id"])
        for key in ("framework", "provision", "title", "summary", "appliesWhen", "why", "kind", "source", "verified", "verification"):
            if key not in o:
                fail(f"obligation {o['id']!r} is missing {key!r}")
        if o["framework"] not in fw_ids:
            fail(f"obligation {o['id']!r} refers to unknown framework {o['framework']!r}")
        if o["kind"] not in ("mandatory", "voluntary", "watch"):
            fail(f"obligation {o['id']!r} has invalid kind {o['kind']!r}")
        for c in o.get("controls", []) + o.get("critical", []):
            if c not in ct_ids:
                fail(f"obligation {o['id']!r} refers to unknown control {c!r}")
    return {
        "knowledgeBaseVersion": fw["knowledgeBaseVersion"],
        "frameworks": frameworks,
        "obligations": obligations,
        "controls": controls,
    }


html = (SRC / "index.html").read_text(encoding="utf-8")
css = (SRC / "styles.css").read_text(encoding="utf-8")
engine = (SRC / "engine.js").read_text(encoding="utf-8")
app = (SRC / "app.js").read_text(encoding="utf-8")
guided = (SRC / "guided.js").read_text(encoding="utf-8")
kb = json.dumps(load_knowledge(), ensure_ascii=False, separators=(",", ":"))

markers = {
    "css": '<link rel="stylesheet" href="styles.css">',
    "kb": '<!-- NAVI_KNOWLEDGE -->',
    "engine": '<script src="engine.js"></script>',
    "app": '<script src="app.js"></script>',
    "guided": '<script src="guided.js"></script>',
}
for name, marker in markers.items():
    if html.count(marker) != 1:
        fail(f"expected exactly one {marker!r} in src/index.html")
for name, code in (("engine.js", engine), ("app.js", app), ("guided.js", guided)):
    if "</script" in code.lower():
        fail(f"{name} contains '</script', which would break inlining")
if "</" in kb:
    kb = kb.replace("</", "<\\/")

html = html.replace(markers["css"], f"<style>\n{css}\n</style>")
html = html.replace(markers["kb"], f'<script id="navi-knowledge" type="application/json">{kb}</script>')
html = html.replace(markers["engine"], f"<script>\n{engine}\n</script>")
html = html.replace(markers["app"], f"<script>\n{app}\n</script>")
html = html.replace(markers["guided"], f"<script>\n{guided}\n</script>")

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
print(f"Built {out.relative_to(ROOT)} ({len(html.encode('utf-8')):,} bytes)")
