#!/usr/bin/env python3
"""Build NAVI Free into a single self-contained index.html for GitHub Pages.

Edit the files in src/ (index.html, styles.css, app.js), then run:

    python3 build.py

The output is ./index.html, with the CSS and JavaScript inlined. One file means
the site works from GitHub Pages, from a downloaded copy, or offline, with no
missing-file problems. No dependencies beyond the Python standard library.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

html = (SRC / "index.html").read_text(encoding="utf-8")
css = (SRC / "styles.css").read_text(encoding="utf-8")
js = (SRC / "app.js").read_text(encoding="utf-8")

link = '<link rel="stylesheet" href="styles.css">'
script = '<script src="app.js"></script>'
for marker in (link, script):
    if html.count(marker) != 1:
        sys.exit(f"build.py: expected exactly one {marker!r} in src/index.html")

if "</script" in js.lower():
    sys.exit("build.py: app.js contains '</script', which would break inlining")

html = html.replace(link, f"<style>\n{css}\n</style>")
html = html.replace(script, f"<script>\n{js}\n</script>")

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
print(f"Built {out.relative_to(ROOT)} ({len(html.encode('utf-8')):,} bytes)")
