# DS 250 Course Site — Gap Analysis & Changes

**Date:** 2026-04-20
**Author:** Chaz Clark (instructor, BYU-Idaho DS 250)
**Scope:** Post-Polars-conversion audit of the public course site, aligning with the Canvas course (master) and Hattie's 3-Phase Learning Model.
**Frameworks used:**
- Hattie, J. (2009). *Visible Learning*. Routledge — Surface / Deep / Transfer phases
- Cognitive Load Theory — intrinsic vs. extraneous vs. germane load
- BYU-Idaho course design conventions — Overview → Content → Teach One Another → Prove It

---

## Why this exists

The site recently completed a pandas → polars conversion. It is intentionally vanilla — the goal of this audit is to flag inconsistencies, extraneous cognitive load, and Hattie-phase gaps that can be addressed with small, targeted changes. No theme work, no heavy restyling, no new frameworks.

Canvas is the authoritative source for assignment names and grading structure. The site is the reference surface students read alongside Canvas. When the two disagree, the site gets updated.

---

## Findings

### 1. Terminology drift — Core Task / Stretch Task

Canvas uses `Core Task 1–3` (1 pt each, pass/fail) and `Stretch Task` (Task 4, 1 pt, pass/fail). The site previously used ~7 patterns:

| Layer | Before | After |
|---|---|---|
| Navbar items | `Task 1–4` | `Core Task 1–3`, `Stretch Task` |
| Page titles | `Unit 1 Task 1:` · `Unit 4, Task 1:` · `Project 5:` · `Unit 4 Stretch:` (one-off) | `Unit N Core Task M: <name>` / `Unit N Stretch Task: <name>` |
| Section header | `Questions and Tasks`, `Questions and Tasks (Core)` (U1 T1+T2 only), `Questions` (U2/U4/U5) | `### Core Questions` / `### Stretch Questions` |
| Body text | "Project Stretchs" (typo × 4 in `Syllabus/competency.qmd`), "Project Stretches", "Stretch Question(s)", "stretch task" | `Stretch Task` (deliverable) / `Stretch Questions` (content) |

Plus visible typos — `menue` (index), `correclty` (~6 pages), `acomplish`, `ofset`, `Febuary` (left in place; referenced by task content).

The Core/Stretch pedagogical distinction (Copilot forbidden on Core, encouraged on Stretch) was defined once — `setup.qmd:40` — and never surfaced on task pages.

### 2. Cognitive load — extraneous friction

- Submission instructions were copy-pasted into every task page (~15 lines × 22 pages). Drift already visible between unit1_task1 and unit2_task1.
- 80+ lines of commented-out sidebar navigation in `_quarto.yml` — Workbooks and Skill Builders files exist but aren't reachable.
- No Canvas cross-reference on task pages — students couldn't tell which site task maps to which Canvas assignment.
- `Projects/project_0.qmd` and `Projects/project_0_dp.qmd` both existed with near-identical content; navbar only linked `_dp`. Canvas mapping was ambiguous.
- Three pages had **silently broken numbered lists** — content between `1.` items broke Pandoc's list continuity, causing later items to re-render as "1." instead of continuing 2, 3, 4.

### 3. Hattie phase gaps

**Surface** — students landed on task pages with no orientation. No Canvas link, no skills preview, no Core-vs-Stretch signal.
**Deep** — tasks live in isolation; no "Task 2 builds on Task 1" framing; no reflection prompts.
**Transfer** — Project 6 (portfolio) isn't framed as the capstone it is.

Note: per-unit overviews are not needed on the site — instructor-recorded unit overview videos are delivered in Canvas.

---

## Scope of this PR

### Tier 1 — accepted, applied in this PR

- **Terminology pass** — normalize navbar items, page titles, section headers, and body text to match Canvas. Fix visible typos.
- **Task-header callout block** — add a lean `.callout-note` at the top of every task page with: Canvas assignment name, Core/Stretch type + grading, and Copilot policy. No time estimates (student ability distribution makes any number misleading); no "you'll practice" line (skills surface via the tag below).
- **Skills tag** — one line `**Skills:** …` immediately under `### Core Questions` / `### Stretch Questions`. Surfaces the Hattie phase-1 priming without per-question authoring.
- **Submission instructions via Quarto include** — replace duplicated block on every task page with `{{< include ../_submission_html.qmd >}}` or `{{< include ../_submission_github.qmd >}}` depending on submission flow. Source of truth in two shared files, no drift.
- **U0 file reconciliation** — rename `Projects/project_0_dp.qmd` → `Projects/project_0.qmd` (the canonical Testing, Testing, 1,2,3 task). Prior `project_0.qmd` (scaffolded variant with walkthrough + meta callouts) removed; git history preserves it. Canvas Task 1 "Setup Checkpoint" intentionally has no site page — it is a Canvas-only self-report of setup status.
- **List-numbering QC fix** — 3 pages had fenced content (iframe, image, paragraph) sitting un-indented between `1.` items, breaking Pandoc's list continuity and silently renumbering subsequent items as "1.". Fixed in `Projects/unit3_task1.qmd`, `Setup/copilot_setup.qmd`, `Setup/quarto_setup.qmd`.

### Tier 2 — accepted, deferred to a later PR

- Project 6 capstone framing — single paragraph at top of `unit6.qmd` naming it as the transfer capstone and tying it to the semester's work.
- Per-task **bolded skill-verb phrasing** at the start of each Core Question (stronger Hattie surface→deep hook). Deferred because it is 70+ individual authoring decisions that are better made semester-by-semester while teaching.

### Out of scope

- Unit-level overview pages (delivered via Canvas videos instead).
- Custom CSS / theme work (site is intentionally vanilla).
- Video embeds (belong in Canvas).
- Reflection prompt callouts (deferred — Canvas already captures this via Teach One Another discussions).
- Time estimates on task pages (too misleading across student ability distribution).

---

## Authoring rule — numbered-list continuity

**Discovered during the list-numbering QC fix. Worth capturing so future edits don't regress.**

Pandoc continues an ordered list across intervening content (paragraph, image, code fence, iframe) only if the content is indented to the width of the list marker. For a `1. ` marker that width is **3 spaces — not 4**.

Wrong (list breaks, next `1.` re-renders as "1"):
```markdown
1. First item

Extra paragraph with context.

1. Second item
```

Right (list continues, next `1.` renders as "2"):
```markdown
1. First item

   Extra paragraph with context.

1. Second item
```

Same rule for images, fenced code blocks, iframes — any non-list block between list items needs 3-space indent to stay inside the preceding item.

---

## Terminology mapping (authoritative for this PR)

| Canvas assignment | Site title | File |
|---|---|---|
| `W01 U0: Core Task 1` (Setup Checkpoint) | — (Canvas-only; student reports setup status) | — |
| `W02 U0: Core Task 2` (Testing, Testing, 1,2,3) | `Unit 0 Core Task 2: Testing, Testing, 1,2,3` | `Projects/project_0.qmd` |
| `W03 U1: Core Task 1` (Exploring Names) | `Unit 1 Core Task 1: Exploring Names` | `Projects/unit1_task1.qmd` |
| `W03 U1: Core Task 2` (Famous Names and You) | `Unit 1 Core Task 2: Famous Names and You` | `Projects/unit1_task2.qmd` |
| `W04 U1: Core Task 3` (Creating New Columns) | `Unit 1 Core Task 3: Creating New Columns` | `Projects/unit1_task3.qmd` |
| `W04 U1: Stretch Task` (Elliot) | `Unit 1 Stretch Task: Elliot` | `Projects/unit1_task4.qmd` |
| `W05 U2: Core Task 1` (Flights: Column Creation) | `Unit 2 Core Task 1: Flights - Column Creation Advanced` | `Projects/unit2_task1.qmd` |
| `W05 U2: Core Task 2` (Flights: Aggregation) | `Unit 2 Core Task 2: Flights - Aggregation` | `Projects/unit2_task2.qmd` |
| `W06 U2: Core Task 3` (Missing Data) | `Unit 2 Core Task 3: Flights - Missing Data & JSON` | `Projects/unit2_task3.qmd` |
| `W06 U2: Stretch Task` (Comparing Delay Types: Pivot) | `Unit 2 Stretch Task: Comparing Delay Types - Pivot` | `Projects/unit2_task4.qmd` |
| `W07 U3: Core Task 1` (DataBaseBall) | `Unit 3 Core Task 1: Baseball Database` | `Projects/unit3_task1.qmd` |
| `W07 U3: Core Task 2` (SQL) | `Unit 3 Core Task 2: Baseball Database (cont.)` | `Projects/unit3_task2.qmd` |
| `W08 U3: Core Task 3` (Joins) | `Unit 3 Core Task 3: Baseball Joins` | `Projects/unit3_task3.qmd` |
| `W08 U3: Stretch Task` (Longevity and Highest Paid Positions) | `Unit 3 Stretch Task: Longevity and Highest Paid Positions` | `Projects/unit3_task4.qmd` |
| `W09 U4: Core Task 1` (Can You Predict That?) | `Unit 4 Core Task 1: Can You Predict That?` | `Projects/unit4_task1.qmd` |
| `W09 U4: Core Task 2` (How Good Is It, Really?) | `Unit 4 Core Task 2: How good is it, really?` | `Projects/unit4_task2.qmd` |
| `W10 U4: Core Task 3` (Show Me) | `Unit 4 Core Task 3: Show me` | `Projects/unit4_task3.qmd` |
| `W10 U4: Stretch Task` (Regression ML) | `Unit 4 Stretch Task: Regression ML` | `Projects/unit4_task4.qmd` |
| `W11 U5: Core Task 1` (Regex) | `Unit 5 Core Task 1: Regular Expression` | `Projects/unit5_task1.qmd` |
| `W11 U5: Core Task 2` (Recoding Variables for ML) | `Unit 5 Core Task 2: Recoding Range Variables` | `Projects/unit5_task2.qmd` |
| `W12 U5: Core Task 3` (Star Wars for Dummies) | `Unit 5 Core Task 3: Star Wars for Dummies` | `Projects/unit5_task3.qmd` |
| `W12 U5: Stretch Task` (Can You Validate Me?) | `Unit 5 Stretch Task: Can you validate me?` | `Projects/unit5_task4.qmd` |
| `W13 U6: Core Task 1` (Git Your DS Portfolio Online) | `Unit 6 Core Task 1: Git Your DS Portfolio Online` | `Projects/unit6.qmd` |

**Note:** 8 site titles differ slightly from Canvas (e.g., "Baseball Database" vs "DataBaseBall", "Flights - Aggregation" vs "Flights: Aggregation"). Site wording was kept; Canvas master is expected to be updated to match on the next sync.

---

## Changes in this PR

### Navigation (`_quarto.yml`)
- Each unit menu: `Task 1-4` → `Core Task 1`, `Core Task 2`, `Core Task 3`, `Stretch Task`
- Top-level `"GitHub Task"` → `"Unit 6 Portfolio"`
- `"Unit 0 Set-up Check"` → `"Unit 0: Testing"` (points at new `project_0.qmd`)
- Removed 3 stale commented-out entries pointing at the removed legacy `project_0.qmd`
- `issue-url` / `repo-url` corrected from `byuidatascience.github.io/...` (Pages URL) to `github.com/byuidatascience/DS250-Course-Polars/` so the "Report an issue" link actually reaches GitHub issues.

### Page titles (23 files)
All 23 task pages normalized to `Unit N Core Task M: <name>` or `Unit N Stretch Task: <name>` form. See terminology mapping table above.

### Section headers (19 files)
- 17 Core task files → `### Core Questions`
- 4 Stretch task files → `### Stretch Questions`
- `project_0.qmd` (renamed): `### Questions and Tasks` → `### Core Questions`
- `unit3_task4.qmd`: kept `### Question 1` / `### Question 2` (different structure by design)

### Task-header callout (23 files)
Lean 3-line `.callout-note` added at the top of every task page (after YAML frontmatter, before `### Background`):

```markdown
::: {.callout-note}
**Canvas:** W05 U2: Core Task 2 — Flights: Aggregation
**Type:** Core Task (1 pt, complete/incomplete)
**Copilot:** Allowed for syntax lookup; disallow for answer generation.
:::
```

Grading is labeled **complete/incomplete** (what students see in SpeedGrader), not `pass/fail` (Canvas config jargon).

### Skills tag (23 files)
One-line `**Skills:** …` added directly under each `### Core Questions` / `### Stretch Questions` header. Skills drafted per task from the question content — see Canvas mapping in the table above.

### Submission includes
- Created `_submission_html.qmd` — collapsible callout with 8-step HTML-upload submission flow
- Created `_submission_github.qmd` — two stacked callouts (instructor guidance + 8-step GitHub Pages publish flow)
- Replaced inline submission blocks on 22 task pages with `{{< include ../_submission_html.qmd >}}` (10 files: U0, U1, U3) or `{{< include ../_submission_github.qmd >}}` (12 files: U2, U4, U5). `unit6.qmd` left as-is (tutorial format, no standard submission block).

### U0 reconciliation (structural)
- Renamed `Projects/project_0_dp.qmd` → `Projects/project_0.qmd`
- Removed the prior `Projects/project_0.qmd` (scaffolded variant with walkthrough video and meta-callouts). Git history preserves the content if a future instructor wants to restore a scaffolded teaching version.
- `_quarto.yml` navbar updated accordingly.

### List-numbering fixes (3 files)
- `Projects/unit3_task1.qmd` — 4-space indent on batting-average Note paragraph changed to 3-space so it continues list item 1.
- `Setup/copilot_setup.qmd` — 4-space indent on inline image changed to 3-space so it continues step 4, preventing steps 5-6 from renumbering to 1-2.
- `Setup/quarto_setup.qmd` — iframe fenced blocks indented to 3 spaces to continue their list items; explicit `3.` restored to `1.` (lazy numbering pattern).

### U6 tab rename (`Projects/unit6.qmd`)
Three `panel-tabset` tabs previously read "Method 1: Use a template", "Method 1: From scratch", "Method 3: GitHub actions" — two labels beginning with "Method 1" were confusing. Relabeled to **Method 1 / Method 2 / Method 3**. Intro prose rewritten to drop references to Quarto's internal 3-way taxonomy — students only need to pick one of the three tabs shown.

### Typo fixes
- `index.qmd`: "menue" → "menu"; subtitle "pandas" → "polars"
- `setup.qmd`: "acomplish" → "accomplish"
- `Syllabus/competency.qmd`: "Stretchs" → "Stretches" (×4), "ofset" → "offset" (×2)
- Task pages: "correclty" → "correctly" in 8 files

---

## Known follow-ups (not in this PR)

- **Canvas master title updates** — 8 task titles on site wording slightly differs from Canvas master (e.g., "Baseball Database" vs "DataBaseBall"). Canvas should be updated to match site wording on next sync.
- **Per-task bolded skill-verb phrasing** — deferred (Tier 2). Better done semester-by-semester while teaching.
- **Project 6 capstone framing** — deferred (Tier 2).
- **Submission flow for `unit6.qmd`** — no standard submission block exists. Leave as-is or add a lightweight submission section? Deferred for instructor decision.
