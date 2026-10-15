# Changelog

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
