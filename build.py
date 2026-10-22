#!/usr/bin/env python3
"""Build NAVI Free into a single self-contained index.html for GitHub Pages.

Edit the files in src/ (index.html, styles.css, engine.js, app.js, guided.js,
retrieval.js, sources.js, the knowledge base in src/knowledge/*.json and the
source library in src/corpus/*.json), then run:

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


SOURCE_TYPES = {"law", "regulatory-standard", "supervisory-expectation", "government-guidance", "standard",
                "industry-good-practice", "regulator-statement", "policy", "navi-guidance"}
BINDINGS = {"mandatory", "voluntary", "watch"}
VERIFICATIONS = {"official-text", "official-page", "secondary", "pending"}
TOPICS = {"strategy", "development", "agents", "data", "model-risk", "security", "privacy", "regulation", "testing",
          "deployment", "monitoring", "third-party", "board", "fairness", "transparency", "genai", "employment",
          "finance", "incidents"}
KB_TYPE = {"law": ("law", "mandatory"), "voluntary": ("standard", "voluntary"), "policy": ("policy", "watch")}


def load_corpus(kb):
    """Build the NAVI source library: the knowledge base converted to passages, plus src/corpus/*.json.

    Every passage must be traceable to a source with a link, a type (law, standard, guidance...), whether it
    is binding, and a verification level and date. Answers built on the library take their legal or
    good-practice labels from this metadata, never from generated text.
    """
    cdir = SRC / "corpus"
    meta = json.loads((cdir / "sources.json").read_text(encoding="utf-8"))
    kb_topics = json.loads((cdir / "kb-topics.json").read_text(encoding="utf-8"))["topics"]
    fw_juris = {"popia": ["za"], "paia": ["za"], "eea": ["za"], "cpa": ["za"], "cybercrimes": ["za"], "kingv": ["za"],
                "za-ai-policy": ["za"], "gdpr": ["eu"], "euaiact": ["eu"], "iso42001": ["intl"], "iso23894": ["intl"],
                "nistairmf": ["intl", "us"], "oecd": ["intl"], "unesco": ["intl"]}
    sources = []
    for f in kb["frameworks"]:
        typ, binding = KB_TYPE[f["type"]]
        if f["id"] == "nistairmf":
            typ = "government-guidance"
        sources.append({"id": f["id"], "title": f["name"], "short": f["short"], "publisher": f.get("typeLabel", ""),
                        "jurisdiction": fw_juris.get(f["id"], ["intl"]), "type": typ, "binding": binding,
                        "status": f["status"], "url": f["source"], "verified": f["verified"],
                        "verification": f["verification"], "fromKnowledgeBase": True})
    sources += meta["sources"]
    passages = []
    for f in kb["frameworks"]:
        passages.append({"id": "kb-fw-" + f["id"], "source": f["id"], "section": "Status", "title": f["name"],
                         "text": f["status"], "topics": ["regulation"] if f["type"] == "law" else ["strategy", "regulation"],
                         "fromKnowledgeBase": True})
    for o in kb["obligations"]:
        if o["id"] not in kb_topics:
            fail(f"src/corpus/kb-topics.json has no topics for obligation {o['id']!r}")
        p = {"id": "kb-" + o["id"], "source": o["framework"], "section": o["provision"], "title": o["title"],
             "text": o["summary"], "topics": kb_topics[o["id"]], "binding": o["kind"], "url": o["source"],
             "verified": o["verified"], "verification": o["verification"], "fromKnowledgeBase": True}
        if o.get("uncertainty"):
            p["uncertainty"] = o["uncertainty"]
        passages.append(p)
    for c in kb["controls"]:
        if c["id"] not in kb_topics:
            fail(f"src/corpus/kb-topics.json has no topics for control {c['id']!r}")
        passages.append({"id": "kb-" + c["id"], "source": "navi-practice", "section": "Safeguard " + c["id"],
                         "title": c["label"], "text": f"{c['help']} What to do: {c['action']} Suggested owner: {c['owner']}.",
                         "topics": kb_topics[c["id"]], "fromKnowledgeBase": True})
    for path in sorted(cdir.glob("passages-*.json")):
        passages += json.loads(path.read_text(encoding="utf-8"))["passages"]

    src_ids = set()
    for s_ in sources:
        sid = s_.get("id")
        if sid in src_ids:
            fail(f"duplicate source id {sid!r}")
        src_ids.add(sid)
        for key in ("title", "short", "jurisdiction", "type", "binding", "status", "url", "verified", "verification"):
            if not s_.get(key):
                fail(f"source {sid!r} is missing {key!r}")
        if s_["type"] not in SOURCE_TYPES:
            fail(f"source {sid!r} has invalid type {s_['type']!r}")
        if s_["binding"] not in BINDINGS or s_["verification"] not in VERIFICATIONS:
            fail(f"source {sid!r} has invalid binding or verification")
        if not s_["url"].startswith("https://"):
            fail(f"source {sid!r} link must be https")
    seen = set()
    for p in passages:
        pid = p.get("id")
        if not pid or pid in seen:
            fail(f"missing or duplicate passage id {pid!r}")
        seen.add(pid)
        for key in ("source", "section", "title", "text", "topics"):
            if not p.get(key):
                fail(f"passage {pid!r} is missing {key!r}")
        if p["source"] not in src_ids:
            fail(f"passage {pid!r} refers to unknown source {p['source']!r}")
        bad = set(p["topics"]) - TOPICS
        if bad:
            fail(f"passage {pid!r} has unknown topics {sorted(bad)}")
        if not 40 <= len(p["text"]) <= 1500:
            fail(f"passage {pid!r} text should be 40-1500 characters (is {len(p['text'])})")
        if "url" in p and not p["url"].startswith("https://"):
            fail(f"passage {pid!r} link must be https")
        if "verification" in p and p["verification"] not in VERIFICATIONS:
            fail(f"passage {pid!r} has invalid verification")
        if "binding" in p and p["binding"] not in BINDINGS:
            fail(f"passage {pid!r} has invalid binding")
    return {"libraryVersion": meta["libraryVersion"], "knowledgeBaseVersion": kb["knowledgeBaseVersion"],
            "sources": sources, "passages": passages}


html = (SRC / "index.html").read_text(encoding="utf-8")
css = (SRC / "styles.css").read_text(encoding="utf-8")
engine = (SRC / "engine.js").read_text(encoding="utf-8")
app = (SRC / "app.js").read_text(encoding="utf-8")
guided = (SRC / "guided.js").read_text(encoding="utf-8")
retrieval = (SRC / "retrieval.js").read_text(encoding="utf-8")
sources_ui = (SRC / "sources.js").read_text(encoding="utf-8")
kb_obj = load_knowledge()
corpus_obj = load_corpus(kb_obj)
kb = json.dumps(kb_obj, ensure_ascii=False, separators=(",", ":"))
corpus = json.dumps(corpus_obj, ensure_ascii=False, separators=(",", ":"))

markers = {
    "css": '<link rel="stylesheet" href="styles.css">',
    "kb": '<!-- NAVI_KNOWLEDGE -->',
    "engine": '<script src="engine.js"></script>',
    "app": '<script src="app.js"></script>',
    "guided": '<script src="guided.js"></script>',
    "corpus": '<!-- NAVI_CORPUS -->',
    "retrieval": '<script src="retrieval.js"></script>',
    "sources": '<script src="sources.js"></script>',
}
for name, marker in markers.items():
    if html.count(marker) != 1:
        fail(f"expected exactly one {marker!r} in src/index.html")
for name, code in (("engine.js", engine), ("app.js", app), ("guided.js", guided),
                   ("retrieval.js", retrieval), ("sources.js", sources_ui)):
    if "</script" in code.lower():
        fail(f"{name} contains '</script', which would break inlining")
kb = kb.replace("</", "<\\/")
corpus = corpus.replace("</", "<\\/")

html = html.replace(markers["css"], f"<style>\n{css}\n</style>")
html = html.replace(markers["kb"], f'<script id="navi-knowledge" type="application/json">{kb}</script>')
html = html.replace(markers["engine"], f"<script>\n{engine}\n</script>")
html = html.replace(markers["app"], f"<script>\n{app}\n</script>")
html = html.replace(markers["guided"], f"<script>\n{guided}\n</script>")
html = html.replace(markers["corpus"], f'<script id="navi-corpus" type="application/json">{corpus}</script>')
html = html.replace(markers["retrieval"], f"<script>\n{retrieval}\n</script>")
html = html.replace(markers["sources"], f"<script>\n{sources_ui}\n</script>")

# The source library is also written as a standalone file for the Phase 2 server and for tests.
(ROOT / "corpus.json").write_text(json.dumps(corpus_obj, ensure_ascii=False, indent=1), encoding="utf-8")

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
# The NAVI API Worker: one self-contained file to paste into Cloudflare (or deploy with wrangler).
worker_src = (ROOT / "worker" / "src" / "worker.js").read_text(encoding="utf-8")
worker_lib = json.dumps(corpus_obj, ensure_ascii=False, separators=(",", ":"))
bundle = ("/* NAVI API Worker - generated by build.py from worker/src/worker.js, src/retrieval.js and the source\n"
          f" * library (version {corpus_obj['libraryVersion']}). Do not edit by hand: edit the sources and run python3 build.py. */\n"
          f"const LIBRARY = {worker_lib};\n\n{retrieval}\n\n{worker_src}")
(ROOT / "worker" / "dist").mkdir(parents=True, exist_ok=True)
(ROOT / "worker" / "dist" / "navi-worker.js").write_text(bundle, encoding="utf-8")

print(f"Built {out.relative_to(ROOT)} ({len(html.encode('utf-8')):,} bytes); "
      f"source library: {len(corpus_obj['sources'])} sources, {len(corpus_obj['passages'])} passages; "
      f"worker/dist/navi-worker.js ({len(bundle.encode('utf-8')):,} bytes)")
