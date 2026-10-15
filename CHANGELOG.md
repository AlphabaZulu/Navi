# Changelog

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
