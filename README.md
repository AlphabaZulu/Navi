# NAVI — From AI ambition to responsible action

**NAVI Free** is a free, no-registration AI governance decision-support tool from Orvendi Group.
It helps individuals and small organisations work out whether an AI use case can and should go
ahead, what safeguards it needs, who should be accountable, and how to record the decision.

Live: https://alphabazulu.github.io/Navi/

- **Ask NAVI** — plain-language questions, answered from a documented rule set (not generative AI)
- **Assess an AI use case** — a guided five-step assessment with an explained outcome
- **My decisions** — saved assessments on your device: reopen, download, delete
- **Explore governance** — a searchable guide, board reflection scenarios and your own reference library
- **NAVI Enterprise** — planned; see the Enterprise page in the app

NAVI's guidance is general and rules-based. It is not legal advice, legal clearance or
organisational approval.

## How it works

- One static page. No server, no accounts, no tracking, no third-party scripts.
- Everything you save stays in your browser's local storage on that device. Download a copy
  from *My decisions* or *About NAVI → Your data and privacy*.
- The risk method is documented in [docs/RISK-METHOD.md](docs/RISK-METHOD.md).

## Repository layout

```
index.html          Built site served by GitHub Pages (do not edit by hand)
src/index.html      Page structure
src/styles.css      Styles and brand tokens
src/app.js          Application logic, assessment engine and content
build.py            Inlines src/ into index.html
tests/              Engine tests and browser end-to-end tests
docs/               Technical assessment, risk method, implementation plan
CHANGELOG.md        Release notes
```

## Making a change

1. Edit the files in `src/`.
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
- **Browser tests** (Chromium) — free access with no registration, landing page, navigation and
  the Back button, a full assessment saved to My decisions, reports, Ask NAVI behaviour, migration
  of pre-2.0 data, export and deletion, persistence, honest dashboard, feedback, enterprise
  interest, layouts at 320–1440px, and accessibility (skip link, accessible names, WCAG AA text
  contrast).

## Privacy and security

- No personal information is needed to use NAVI.
- Feedback and enterprise-interest forms only *prepare* an email. You review it and send it from
  your own mail app.
- A Content-Security-Policy blocks all external requests.
- Local browser storage is not encrypted. Don't store confidential material on shared devices.
- People who used the earlier version with a sign-up form can delete those saved sign-up details
  from *About NAVI*.

## Roadmap

See [docs/IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md). Next up (Phase 2): a verified,
source-referenced regulatory knowledge base with jurisdiction-aware applicability, a deeper
assessment (inherent vs residual risk, control gaps), clarifying questions in Ask NAVI, and a
full decision report.

© Orvendi Group. Feedback: use the Feedback page in the app.
