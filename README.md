# NAVI — From AI ambition to responsible action

**NAVI Free** is a free, no-registration AI governance decision-support tool from Orvendi Group.
It helps individuals and small organisations work out whether an AI use case can and should go
ahead, what safeguards it needs, who should be accountable, and how to record the decision.

Live: https://alphabazulu.github.io/Navi/

- **Guided NAVI** (optional, for beginners) — *New to NAVI? Let us guide you.* One plain-language question at a time, with help, examples and an "I'm not sure" option, layered answers and plain-language results. Same engine and records as Standard NAVI; switch either way at any point. See [docs/GUIDED-EXPERIENCE.md](docs/GUIDED-EXPERIENCE.md)
- **Ask NAVI** — plain-language questions with targeted follow-up questions, answered from a documented rule set (not generative AI)
- **Assess an AI use case** — a guided five-step assessment: requirements that may apply, inherent and residual risk, control gaps, actions, and a 12-section Decision & Action Report
- **My decisions** — saved assessments on your device: reopen, download, delete
- **Explore governance** — a searchable guide, **NAVI Sources** (145 cited summaries of laws, regulations, standards and guidance, searchable offline), board reflection scenarios and your own reference library
- **NAVI Enterprise** — planned; see the Enterprise page in the app

NAVI's guidance is general and rules-based. It is not legal advice, legal clearance or
organisational approval.

## How it works

- One static page. No server, no accounts, no tracking, no third-party scripts.
- Everything you save stays in your browser's local storage on that device. Download a copy
  from *My decisions* or *About NAVI → Your data and privacy*.
- The risk method is documented in [docs/RISK-METHOD.md](docs/RISK-METHOD.md); the knowledge base,
  how to update it and the verification log are in [docs/KNOWLEDGE-BASE.md](docs/KNOWLEDGE-BASE.md).

## Repository layout

```
index.html          Built site served by GitHub Pages (do not edit by hand)
src/index.html      Page structure
src/styles.css      Styles and brand tokens
src/engine.js       Assessment engine: risk rules, knowledge-base evaluator, residual risk
src/app.js          User interface, guide and reflection content
src/guided.js       Optional Guided NAVI layer (uses the same engine via window.NAVI)
src/retrieval.js    Source library search (shared with the planned AI server)
src/sources.js      NAVI Sources page and related passages for the assistants
src/corpus/         Source library: sources and passages beyond the knowledge base, as JSON
corpus.json         Built source library (written by build.py; do not edit by hand)
eval/               120-question evaluation set and the retrieval report
worker/             NAVI API Worker (Cloudflare): src/worker.js, wrangler.toml, dist/navi-worker.js (built)
src/knowledge/      Governance knowledge base (frameworks, obligations, controls) as JSON
build.py            Inlines src/ into index.html
tests/              Engine tests and browser end-to-end tests
docs/               Technical assessment, risk method, knowledge base, data model, plan, guided experience
CHANGELOG.md        Release notes
```

## Making a change

1. Edit the files in `src/`. To update regulatory content, edit `src/knowledge/*.json` only
   (see [docs/KNOWLEDGE-BASE.md](docs/KNOWLEDGE-BASE.md)); no code changes are needed.
2. Build: `python3 build.py` (Python 3, standard library only).
3. Test: `npm install`, then `npx playwright install chromium` (first time only), then `npm test`.
4. Commit both `src/` and the rebuilt `index.html`.

## Deploying to GitHub Pages

The repository is already set up: **Settings → Pages → Deploy from a branch → `main` / root**.
Every push to `main` that changes `index.html` goes live within a minute or two.

To update without git: on GitHub, open `index.html` → **Edit** (or **Add file → Upload files** and
replace it), upload the newly built file, and commit. Upload the changed `src/`, `docs/` and
`tests/` files the same way so the source stays in step with the live site.

## Testing

`npm test` builds the site and runs:

- **Engine tests** — all 35,000 input combinations match the recorded baseline; determinism;
  hard rules; labels never claim permission or approval.
- **Knowledge-base tests** — every entry sourced, dated and consistent; voluntary standards never
  mandatory; applicability across eight sector and jurisdiction scenarios; every residual-risk rule.
- **Browser tests** (Chromium) — free access with no registration, landing page, navigation and
  the Back button, the five-step assessment, jurisdiction-aware requirements, residual risk, the
  12-section report and JSON record, Ask NAVI follow-up questions, migration
  of pre-2.0 data, export and deletion, persistence, honest dashboard, feedback, enterprise
  interest, layouts at 320–1440px, and accessibility (skip link, accessible names, WCAG AA text
  contrast).
- **Guided tests** — guided and standard give identical results for the same answers; "I'm not
  sure" never lowers risk; Back, review and switching keep every answer; draft resume; plain
  results and report; guided Ask NAVI layers; keyboard-only use; 320/375px; contrast.
- **Source library tests** — every passage sourced, dated, linked and classified; the knowledge
  base included unchanged; coverage of every governance area; search finds a suitable passage
  for at least 90% of the evaluation questions and flags off-topic ones; the NAVI Sources page,
  related passages in Ask NAVI and Guided NAVI, no network requests, 320/375px, contrast.
- **Worker tests** — the NAVI API server with a simulated model and a mocked model API: origin and
  input checks, privacy masking, per-visitor limits, daily spending cap, caching, citation and
  wording checks, prompt-injection resistance, fallbacks, and every evaluation question.

## Privacy and security

- No personal information is needed to use NAVI.
- Feedback and enterprise-interest forms only *prepare* an email. You review it and send it from
  your own mail app.
- A Content-Security-Policy blocks all external requests.
- Local browser storage is not encrypted. Don't store confidential material on shared devices.
- People who used the earlier version with a sign-up form can delete those saved sign-up details
  from *About NAVI*.

## Roadmap

The open-ended AI governance assistant is approved and being built in four phases; Phase 1 (the
source library and offline search) is complete. See [docs/OPEN-ENDED-ASSISTANT.md](docs/OPEN-ENDED-ASSISTANT.md)
and [docs/SOURCE-LIBRARY.md](docs/SOURCE-LIBRARY.md).


See [docs/IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md). Phases 1 and 2 are complete. Next
(Phase 3): edit saved decisions, notes, action tracking, import of exported records, a rebuilt
personal dashboard, and an optional governance maturity questionnaire.

© Orvendi Group. Feedback: use the Feedback page in the app.
