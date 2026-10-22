# Changelog

## NAVI Free 2.3 — Optional AI answers (Phase 3, 22 October 2026)

**Why:** answer any legitimate AI governance question in context, from cited sources, without
changing how NAVI's formal risk check works.

- Ask NAVI: new **Answer type** choice. The rules-based check stays the default and is unchanged.
  *AI answer from NAVI's sources* is optional and needs the privacy notice to be accepted first.
- Answers are pitched for someone new, a developer or specialist, or an executive or board member,
  and show labelled, numbered citations, uncertainty, more detail and the sources with links.
- *Run NAVI's formal check* hands any question to the rules engine for a risk classification.
- Guided NAVI offers AI answers in plain language, in its three layers.
- Personal details are masked in the browser before sending, and again on the server. Saved
  assessments never leave the device. AI choices are listed under Your data and privacy and can be
  withdrawn there.
- If the AI service is unavailable or the limit is reached, NAVI shows the closest offline sources.
- Source library 2026.10.22: all passages verified (32 against official text, 69 against official
  pages, 44 against reputable secondary sources); NIST, SP 800-218A and ISO 23894 wording corrected.
- Worker 2.3.0: shorter fallback summaries.
- 7 new tests (80 in total).

## NAVI API Worker — Phase 2 (20 October 2026)

**Why:** AI answers need a server that keeps the API key secret, protects privacy and cost, and
checks every answer before anyone sees it. The website itself is unchanged in this release.

- New `worker/`: a Cloudflare Worker (`navi-api.orvendi.workers.dev`) built into one file,
  `worker/dist/navi-worker.js`, with the source library and search built in.
- Only the NAVI site may call it; questions are limited to 1,500 characters and six earlier turns.
- Email addresses, phone numbers, SA ID numbers and card numbers are masked before anything else.
- Per-visitor limits (20 an hour, 50 a day), a US$2 daily spending cap, and a 24-hour cache for
  repeated questions.
- The model must answer only from the passages retrieved for the question, in a fixed JSON format.
  Answers that cite anything else, make uncited points, give risk scores, ratings, approvals,
  compliance claims or legal opinions, or repeat the instructions are retried once and then
  replaced by a sources-only answer. Legal or good-practice labels come from library metadata.
- Starts in simulated mode (answers from the sources, no model call, no cost); `MODEL_MODE=live`
  is switched on at the Phase 3 gate.
- 15 new tests (73 in total). Deployment guide in `docs/WORKER-DEPLOYMENT.md`.

## NAVI Free 2.0 — Source library (19 October 2026)

**Why:** NAVI should give useful, cited guidance on governance questions it was never programmed
for. This is Phase 1 of the approved open-ended assistant: the trusted material and the search
that future AI answers will be built on, already useful without any AI.

- New **NAVI Sources** page (Explore governance): search 145 passages from 28 sources: laws,
  regulations, standards and guidance on AI strategy, development, agents, data, model risk,
  security, privacy, regulation, testing, deployment, monitoring, third-party AI and board
  oversight, including South African financial-sector and Information Regulator material.
- Every passage shows whether it is a **legal requirement**, **good practice** or on the **watch
  list** (taken from the source's metadata), who it applies to, a link to the original, and when
  and how NAVI checked it.
- Filters for jurisdiction, kind and topic; topic browsing; honest "may not cover this" notice.
- Ask NAVI and Guided NAVI now show the closest source passages when a question isn't about a
  specific use case, instead of only asking for more detail. Recognised use cases are unchanged.
- Search runs on the device; nothing is sent anywhere.
- 120-question evaluation set (40 held back). Search finds a suitable source in the top five for
  99% of development questions and 97% of held-back questions.
- **Unchanged:** risk engine (35,000-combination baseline matches), knowledge base, assessments,
  records, reports, Guided NAVI, privacy and storage.
- 10 new tests (58 in total).

## NAVI Free 2.0 — Guided Experience (15 October 2026)

**Why:** people new to AI governance should be able to get the same answer as experienced users,
without needing to know the terms first.

- New, optional **Guided NAVI**. Start from "New to NAVI? Let us guide you." → *Guide Me* on the
  home page.
- Welcome screen with four choices: ask a question, check an AI tool or idea, understand AI
  governance, see previous work.
- Guided assessment: one question at a time in plain language, with examples, *I'm not sure*,
  Back/Continue, a progress bar, *What does this mean? / Show me an example / Why are you asking?*
  help, and a review screen. Unfinished checks are saved on the device and can be resumed.
- *I'm not sure* never lowers risk: each one is treated cautiously and listed as an assumption in
  the result and report.
- Guided Ask NAVI: five suggested questions, follow-up questions, and answers in three layers
  (simple answer · what you should consider · full detail). States clearly that NAVI is not an AI
  chatbot and what it can't answer.
- Plain-language results: *What did NAVI find? · What does this mean for you? · What should you do
  next? · Would you like more detail?*, plus the full result, the 12-section report and a simple
  printable summary.
- Switch between Guided and Standard NAVI at any point, both ways, without losing answers.
- **Unchanged:** risk method (the 35,000-combination baseline still matches), knowledge base,
  standard assessment, Ask NAVI, reports, record format (guided records add two optional fields),
  storage and navigation.
- 10 new browser tests (48 in total). Design, architecture and a beginner usability test plan are
  in `docs/GUIDED-EXPERIENCE.md`.

## NAVI Free 2.0 — Phase 2 (15 October 2026)

**Why:** answers should be specific to the person's situation, traceable to verified sources,
and honest about what is law, what is good practice and what NAVI had to assume.

### Verified governance knowledge base
- New `src/knowledge/` files: 14 frameworks, 31 obligations and 16 safeguards. Each entry has its
  provision, plain-language summary, applicability conditions, mandatory or voluntary status,
  required controls, uncertainty notes, source link, last-checked date and verification level.
- Status and dates re-verified on 15 October 2026 (see `docs/KNOWLEDGE-BASE.md`). Notable updates:
  - EU AI Act amended by Regulation (EU) 2026/1744: Annex III high-risk requirements (e.g.
    recruitment, credit) now apply from **2 December 2027**, not 2 August 2026.
  - Employment Equity Act s8: the certification requirement was deleted from 1 January 2025.
  - Cybercrimes Act s54 (72-hour reporting) was excluded from the 2021 commencement and is shown
    as "check status".
  - South Africa's National AI Policy: draft withdrawn; shown as a watch item, not an obligation.
- **GDPR and King V are no longer added to every assessment.** Requirements now depend on the
  jurisdictions, data, people, autonomy, tool and hosting location. Voluntary codes and standards
  are never presented as mandatory.
- About NAVI's framework table is generated from the knowledge base.

### Deeper assessment
- Five steps: define the use case (name, description, objective, sector, jurisdictions, autonomy,
  stage, users, affected people), what the AI does, data and technology, impact on people
  (including an EU AI Act prohibited-practice check), and safeguards already in place.
- Results show inherent vs **residual** risk, **governance readiness**, a **"Can we do this?"**
  permissibility indicator, requirements grouped as legal vs voluntary with sources, safeguards in
  place vs **control gaps**, a prioritised **action plan** with suggested owners, reviews and
  approvals, when to get specialist advice, and assumptions.
- After an assessment, the wizard is replaced by the result, with *Edit answers* and *New assessment*.

### Ask NAVI follow-up questions
- NAVI asks up to six targeted questions (countries involved, hosting location, tool, whether a
  person makes the final decision, human review, fairness testing) with one-tap answers. You can
  also type an answer or skip; skipped answers become cautious, stated assumptions.
- Answers separate legal requirements from voluntary standards, flag items needing expert review,
  and say when to involve legal, privacy or cyber-security specialists.
- *Turn this into a full assessment* carries the answers into a pre-filled assessment.

### Reports and records
- New **Decision & Action Report** with 12 sections: executive summary, use-case description,
  requirements, risks and impacts, existing safeguards, control gaps, actions, accountable roles,
  reviews and approvals (with a sign-off table), references, limitations and assumptions, and next
  steps. Print, or save as PDF from the print dialog.
- **Download decision record (JSON)**: structured export (`docs/DATA-MODEL.md`).
- Saved decisions now store the full inputs, so reopening one reproduces the complete result.
  Decisions saved before 2.0 still open, with a notice about what was assumed.

### Quality
- The engine is now a separate, pure module (`src/engine.js`). The 35,000-combination inherent-risk
  fingerprint is unchanged.
- 38 automated tests (up from 19): knowledge-base integrity, applicability across 8 sector and
  jurisdiction scenarios, every residual-risk rule, the wizard, follow-up conversations, the
  12-section report, JSON export, and mobile layouts of the result and report.
- Fixed: hidden screen-reader text inside wide tables widened the page on phones.

## NAVI Free 2.0 — Phase 1 (13 October 2026)

**Why:** NAVI should be free to use from the first click, honest about what it is, and clear
that it supports decisions rather than approving them.

### Access
- Removed the sign-up gate, the splash page and the "Full access" badges. Every feature opens
  immediately, with no registration, payment or trial.
- Data saved by the earlier version (decisions, documents, feedback) is kept. Old sign-up details
  are no longer used, aren't deleted silently, and can be removed from *About NAVI*.

### Experience
- New landing page: "Make informed, responsible and accountable AI decisions", four entry points
  (Ask NAVI, Assess an AI use case, Manage my decisions, Explore AI governance), Start free, the
  five questions, and NAVI Free vs NAVI Enterprise.
- Navigation regrouped into primary and secondary menus. Pages have their own URLs (e.g.
  `#assessment`), so they can be bookmarked and the Back button works. New mobile menu; layouts
  checked from 320px to 1440px.
- New pages: **My decisions**, **NAVI Enterprise** (clearly marked planned, with a consent-based
  "register interest" email), **About NAVI** (how NAVI works, limitations, framework status,
  privacy and data controls).
- "Reference Documentation" renamed **Reference Library**.

### Trust and accuracy
- Outcomes now describe risk ("Lower governance risk", "Elevated risk — safeguards needed",
  "High risk — escalate before proceeding") instead of "Permitted / Not permitted".
- Every result and report carries a decision-support disclaimer.
- "Confidence %" (a heuristic) is replaced by the actual **rule score out of 16** with its
  thresholds; documented in `docs/RISK-METHOD.md`.
- "Applicable regulations" is now **Frameworks that may apply**, with a note that applicability
  depends on jurisdiction. About NAVI marks which frameworks are law and which are voluntary.
- Approvers are now **suggested accountable people**.
- **Ask NAVI** says plainly that it is rules-based, not generative AI. It marks which factors it
  assumed, asks for more detail instead of answering unrecognised questions, and only saves an
  answer when you choose to.
- Fixed: a bare "ChatGPT" (or Gemini, Claude, etc.) was treated as an enterprise edition, so
  "customer complaints into ChatGPT" came back lower risk. It is now treated as a public tool
  (high risk with personal data). "Shortlist job applicants" is now recognised as recruitment.
- The dashboard's "governance maturity" is relabelled an **indicative readiness score**, and the
  dashboard counts only decisions you saved.

### Accessibility
- WCAG AA text contrast across the app: darker teal for text and links, charcoal text on teal
  buttons, darker grey, amber and green. Skip link, `aria-current`, focus moves to each new page's
  heading, labelled charts, accessible star rating, reduced-motion support.

### Privacy and security
- Feedback email is optional (the prepared email already comes from your own address).
- Content-Security-Policy added. Warning added before storing documents. "Download all my data"
  and "Delete all my NAVI data" controls added.

### Engineering
- Editable source in `src/`, with `build.py` producing the single-file site.
- 19 automated tests (engine and browser). The engine classifies all 35,000 input combinations
  exactly as before.
- Docs: technical assessment, risk method, implementation plan, README.

### Still planned
Phase 2: verified regulatory knowledge base, jurisdiction-aware applicability, deeper assessment,
Ask NAVI clarifying questions, 12-section decision report. Phase 3: editing, notes, action
tracking, import, rebuilt dashboard. Phase 4: enterprise architecture. See
`docs/IMPLEMENTATION-PLAN.md`.
