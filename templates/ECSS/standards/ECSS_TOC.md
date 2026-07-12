# Adding SECTION hierarchy to ECSS `.sdoc` files

This document describes the task performed on `docs/ecss/ECSS-E-ST-40C Rev.1.sdoc`
(adding a `[[SECTION]]` hierarchy derived from the source PDF) and the requirements
needed to repeat it for the other ECSS `.sdoc` files obtained from the ECSS EARM matrix: https://ecss.nl/earm/.

## Starting point / problem

These `.sdoc` files were generated from ESA EARM Excel exports, which are flat:
`[DOCUMENT]` → `[GRAMMAR]` → a long flat list of `[REQUIREMENT]` blocks, with no
`SECTION` nodes. The Excel source has no section/chapter structure, but the
original PDF standard does (numbered clauses and annexes with real titles). The
task is to reconstruct that structure as nested `[[SECTION]]` nodes around the
existing requirements, without touching the requirements themselves.

## Key fact: `ECSS_REQ_ID` already encodes the hierarchy path

Every requirement has an `ECSS_REQ_ID` field whose value is literally its position
in the standard's clause/annex tree, e.g.:

- `5.2.2.1a` → clause `5` → `5.2` → `5.2.2` → `5.2.2.1`, requirement letter `a`
  (siblings `b`, `c`, ... share the same leaf clause/section).
- `B.2.1<4.1>a` → Annex `B` → `B.1`/`B.2`/`B.2.1` → sub-item `<4.1>` → letter `a`.
  This `<LETTER>.2.1<key>` pattern holds for every DRD annex (in the 40C doc:
  B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,T). `<key>` may be one level (`<3>`) or two
  (`<4.1>`).
- Occasional flatter forms exist per-document (e.g. `R.2a` in the 40C doc — Annex
  R has only one requirement, no bracket). Always grep the actual file first:
  ```
  grep "ECSS_REQ_ID:" "<file>.sdoc" | sed 's/ECSS_REQ_ID: //' | sort -u
  ```
  and look at the distinct prefixes/shapes before assuming the pattern above
  applies unchanged.

This means the section tree can be derived mechanically from `ECSS_REQ_ID`
values already in the file — the PDF is only needed to supply the human-readable
**titles** for each clause/annex/sub-item number.

## Extracting titles from the PDF

1. `pdftotext -layout "<file>.pdf" out.txt` (needs `cryptography` installed in the
   venv if the PDF is encrypted — `pip install cryptography`, then pypdf/pdftotext
   work).
2. The PDF's own Table of Contents (first few pages) gives exact titles for
   clause levels 1–3 (e.g. `5.2.2 Software related system requirements
   analysis`) and for every Annex's top-level title (e.g. `Annex B (normative)
   Software system specification (SSS) - DRD`).
3. Deeper headings (clause level 4, and annex `<n>`/`<n.m>` sub-items) are **not**
   in the ToC — they appear inline in the body text, immediately followed by the
   requirement's `UID` (right-aligned, e.g. `ECSS-E-ST-40_0860001`) and then the
   lettered requirement text:
   ```
   5.2.2.1        Specification of system requirements allocated to
                  software
                                                    ECSS-E-ST-40_0860001
   a.  The customer shall derive system requirements allocated to software...
   ```
   Cross-reference by the `UID` (unique, already in the `.sdoc` file) to reliably
   anchor a PDF location to a specific `[REQUIREMENT]` block — do not try to match
   on clause numbers alone, since numbers also appear in running headers/footers
   and page numbers.
4. Never invent a title. If a heading can't be found confidently in the PDF text,
   fall back to the bare clause/annex number as the title rather than guessing.
5. Some documents have clause levels with **no heading text anywhere in the
   source**, not just hard-to-find — e.g. in the Q-ST-80C Rev.2 doc, level-4
   clause numbers (`5.1.3.1`, `6.2.4.5`, ...) have only a bare placeholder in the
   PDF, no title at all (confirmed via `pdftotext -layout`). In that case, do
   **not** fabricate a title and do not repeat/duplicate the parent's title —
   instead stop the `[[SECTION]]` hierarchy one level above the untitled level.
   No information is lost: the full clause number (including the untitled leaf
   level) is still visible via each requirement's own `ECSS_REQ_ID` field. Before
   applying this, double check the level is *genuinely* untitled everywhere (not
   just missing from the ToC) — a single exception among many siblings (e.g. one
   clause out of a dozen that *does* have a title) should still get its own
   section if it has requirement descendants, per the general rule above.

## Which headings get a SECTION

- Every heading level down to the leaf clause (4 levels for clause 5; annex
  letter → `X.2.1` → `<n>` → `<n.m>` for DRD annexes) gets its own `[[SECTION]]`,
  full depth, matching the PDF numbering and titles exactly.
- Skip headings that have **zero requirement descendants** — e.g. clause `5.1
  Introduction`, or annexes that are purely informative and contain no
  requirements at all (in the 40C doc: Annex A, Q, S, U). Check this with the
  `ECSS_REQ_ID` prefix grep above before starting.

## StrictDoc syntax requirements (version 0.26.0 in this repo's `.venv`)

- Use the **new composite-node syntax**: `[[SECTION]]` / `[[/SECTION]]` (double
  brackets). The old single-bracket `[SECTION]` is deprecated and hard-errors on
  export in this StrictDoc version.
- Add an explicit `SECTION` element to the `[GRAMMAR]` block (recommended even
  though StrictDoc will improvise one if omitted):
  ```
  - TAG: SECTION
    PROPERTIES:
      IS_COMPOSITE: True
      PREFIX: None
      VIEW_STYLE: Narrative
    FIELDS:
    - TITLE: MID
      TYPE: String
      REQUIRED: False
    - TITLE: UID
      TYPE: String
      REQUIRED: False
    - TITLE: LEVEL
      TYPE: String
      REQUIRED: False
    - TITLE: TITLE
      TYPE: String
      REQUIRED: True
  ```
- Each `[[SECTION]]` gets:
  ```
  [[SECTION]]
  LEVEL: None
  TITLE: 5.2.2.1 Specification of system requirements allocated to software

  ...children...

  [[/SECTION]]
  ```
  `TITLE:` carries the real clause/annex number as plain text (so the number is
  always visible, regardless of StrictDoc's own numbering).

  `LEVEL: None` is the deliberate final choice — see next section.

## `LEVEL` field: why `None`, and the alternative that was rejected

StrictDoc auto-numbers sections by default (`AUTO_LEVELS: On`), which would
produce sequential numbers (`1`, `1.1`, `1.1.1`, ...) unrelated to the real ECSS
clause numbers already embedded in `TITLE`. Two ways to avoid the collision were
tested:

1. **`LEVEL: None` on every section (chosen).** Suppresses StrictDoc's own
   numbering entirely; the real number is only shown via `TITLE` text. Requires
   no change to `AUTO_LEVELS` (stays at its default) and no change to any
   `[REQUIREMENT]` block.
2. **Explicit real-number `LEVEL` per section, still with `AUTO_LEVELS` at
   default** (e.g. `LEVEL: 5.2.2.1`) — also works and additionally makes
   StrictDoc's TOC/`data-level` attribute show the real number. This was
   implemented and verified at one point in this task, then reverted back to
   option 1 by explicit user request, since the number is already visible in
   `TITLE` and duplicating it in `LEVEL` was judged redundant.

   Do **not** use `OPTIONS: AUTO_LEVELS: Off` at the document level — this was
   tried and rejected because StrictDoc then requires an explicit `LEVEL` field
   on **every** node lacking a `TITLE` field, including plain `[REQUIREMENT]`
   blocks (confirmed against StrictDoc's own test fixture
   `tests/integration/features/sdoc/LEVEL/AUTO_LEVELS/02_option_is_off/`), which
   would mean touching all requirement blocks — a hard violation of the
   "never alter existing requirements" constraint.

## Hard constraints (do not violate)

1. Never alter any existing `[REQUIREMENT]` block's fields, field order, or
   text content — only insert `[[SECTION]]` / `LEVEL` / `TITLE` /
   `[[/SECTION]]` lines around/between existing blocks, and add the `SECTION`
   grammar element.
2. Preserve the exact original order of all requirements.
3. Every requirement ends up inside some leaf `SECTION`.

## Recommended process

1. Do the transform with a script (not manual editing) — these files are
   thousands of lines and hand-editing risks silent corruption.
2. Build a title map keyed by the exact `ECSS_REQ_ID`-prefix hierarchy (e.g.
   `5`, `5.2`, `5.2.2`, `5.2.2.1`, ..., `B`, `B.2.1`, `B.2.1.4`, `B.2.1.4.1`, ...)
   from the PDF text, anchored via requirement `UID`s as described above.
3. Walk the `.sdoc` file's requirements in order; whenever the hierarchy path
   implied by `ECSS_REQ_ID` changes, close/open the right `[[SECTION]]` nodes,
   pulling `TITLE` text from the map (skipping heading levels with no
   requirement descendants).
4. Verify before considering it done:
   - Requirement count unchanged (`grep -c "^\[REQUIREMENT\]"`).
   - `git diff` on the file shows **only insertions**, zero deletions/changes
     (confirms nothing existing was touched).
   - `[[SECTION]]` / `[[/SECTION]]` counts are equal (balanced).
   - `strictdoc export --formats=html "<file>.sdoc" --output-dir <tmp>` completes
     with no errors.
   - Spot-check rendered HTML/TOC titles across a few different clauses and at
     least two different annexes.
