# Rant Circle — Master Roadmap
## Worksheet Generator

**Project:** Rant Circle Worksheet Generator
**Business:** Primo English | 서울 프리미엄 원어민 영어 코칭
**Program:** Rant Circle — group English conversation class structured around peer venting and advice
**Owner:** Primo English (eth4nh4rdy)
**Status:** Pre-development
**Last updated:** 2026-09-03

---

## What Rant Circle Is

Rant Circle is a flexible group English class format for 3–5 students. Students share real-life problems or frustrations in English and receive peer advice from the group. Participation is fluid — some students rant and receive advice, others may choose to only give advice on a given day. Class structure is determined by the students and teacher in the room, not by fixed rules.

The worksheet generator produces a custom DOCX worksheet packet for each session: a Speaker Prep Sheet for each ranting student, Listener Notes pages for all other students, a shared Language Focus Card tailored to the session topic, and a Post-Class Reflection sheet. Output is driven entirely by CLI flags.

---

## Program Design

### Flexibility Principles
- Not all students need to rant in every session
- Some students may attend only to give advice
- Order of speakers can be random (dice roll), volunteered, or teacher-directed
- The worksheet adapts to however many ranters are expected — it does not enforce a number
- 60 minutes is the target — pacing is the teacher's job, not the worksheet's

### Suggested Session Arc (flexible)
| Phase | Description | Approx. Time |
|---|---|---|
| Warm Circle | One sentence check-in from everyone | 5–10 min |
| Rant Round(s) | Each ranting student shares; group listens, asks, advises | 12–17 min per ranter |
| Language Wrap | Teacher highlights strong phrases and patterns from the session | 5–7 min |

### Group Size
- **Ideal:** 3 students (everyone can rant in 60 minutes)
- **Workable:** 4–5 students (not everyone may rant — flexible by design)
- **Minimum:** 2 students (one ranter, one advisor — reduced but functional)

---

## Worksheet Structure

All pages are produced as a single DOCX file per session. Page count scales with `--ranters` flag.

### Page 1 — Language Focus Card *(always 1 page)*
- Session header: Rant Circle logo title, date, topic
- Empathy openers (e.g. *"That sounds really frustrating..."*)
- Hedged advice phrases (e.g. *"You might want to consider..."*)
- Strong advice phrases (e.g. *"If I were you, I'd..."*)
- Pushback language (e.g. *"I see it a little differently..."*)
- Phrases tailored to session topic when `--topic` is provided
- Fallback to general phrase bank when no topic is given
- Students expected to use at least 2 phrases from this card during the session

### Page 2 — Warm Circle Check-In *(always 1 page)*
- One row per student: Name / Right now I'm feeling ___ because ___
- Rows scale with `--students` flag (default: 3)

### Pages 3+ — Speaker Prep Sheets *(1 page per ranter)*
- Generated per ranter: count driven by `--ranters` flag
- Fields:
  - Name / Session date
  - My situation in one sentence
  - The main feeling I'm having
  - What I've already tried or considered
  - What kind of support I'm looking for (checkbox: Practical advice / Just to vent / Reality check / All of the above)
  - 3 words or phrases I might need help saying in English

### Listener Notes Sections *(1 section per ranter, per listener)*
- Grouped after all Speaker Prep Sheets
- Each section has fields for:
  - Speaker name / Topic (brief)
  - While they spoke, I noticed: ___
  - A clarifying question I want to ask: ___
  - My advice (use a phrase from the Language Focus Card): ___
  - One thing they said that resonated with me: ___
- Layout: each listener gets one section per ranter (e.g. 3 ranters = 3 sections per listener)
- Sections separated by clear dividers, not page breaks (space-efficient for printing)

### Final Page — Post-Class Reflection *(always 1 page)*
- Session date
- Advice I appreciated today — one entry per ranter:
  - From [Ranter name]: ___
  - (rows scale with `--ranters` flag)
- A phrase I used today that I'm proud of: ___
- A phrase I heard that I want to use again: ___
- Something I want to say better next time: ___
- My topic for next session (if I want to go again): ___

---

## CLI Interface

```bash
python main.py --ranters 2 --students 4 --topic "work hours" --date 2026-09-10
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--ranters` | int | 2 | Number of students expected to rant |
| `--students` | int | 3 | Total number of students in the session |
| `--topic` | str | None | Topic slug from `topics.yaml` — drives Language Focus Card |
| `--date` | str | today | Session date (YYYY-MM-DD) — defaults to current date |
| `--out` | str | `./output` | Output directory |

### Output Filename Convention
```
rant_circle_YYYYMMDD_R{ranters}S{students}.docx
```
Example: `rant_circle_20260910_R2S4.docx`

---

## File Structure

```
rant_circle/
├── main.py                  # CLI entry point and pipeline orchestrator
├── generator.py             # LLM call for Language Focus Card (topic-driven)
├── formatter.py             # DOCX rendering — all page types
├── topics.yaml              # Topic slugs, categories, display names, phrase hints
├── phrases.yaml             # General empathy and advice phrase bank (static fallback)
├── .env                     # API key — never committed
├── .env.example             # Key template — committed
├── .gitignore
├── requirements.txt
└── output/
    └── .gitkeep
```

---

## Topic Suggestion List (`topics.yaml` seed)

### Work & Career
- `work-hours` — Overwork, overtime, work-life balance
- `difficult-coworker` — Conflict with a colleague
- `bad-boss` — Management problems, feeling unsupported
- `career-direction` — Not knowing what career path to take
- `job-change` — Thinking about quitting or switching jobs
- `workplace-culture` — Office environment, company values clash

### Relationships
- `friendship` — A friendship that has changed or feels one-sided
- `romantic` — Romantic relationship stress or confusion
- `family-pressure` — Expectations or conflict with family
- `parent-conflict` — Specific tension with parents
- `feeling-misunderstood` — Not being heard or seen by people close to you

### Life Decisions
- `study-abroad` — Whether to go, where, when
- `quitting` — Giving up on something — a goal, a job, a habit
- `commitment` — Afraid to commit to a path or decision
- `life-direction` — Broader uncertainty about what you want

### Identity & Feelings
- `comparison` — Feeling behind compared to peers
- `imposter-syndrome` — Doubting your abilities or belonging
- `burnout` — Exhaustion, low motivation, emptiness
- `social-anxiety` — Discomfort in social situations
- `not-enough` — Feeling like you're not good enough

### Everyday Frustrations
- `recurring-situation` — Something that keeps bothering you
- `unfair-treatment` — A situation that felt unjust
- `bad-habit` — A habit you want to break but can't
- `general` — No specific topic — general life frustration

---

## Phase Breakdown

---

### Phase 0 — Design, Specification & Repository Setup

**Goal:** Lock all design decisions and establish the project repository before any code is written.

#### Tasks

**0.1 — GitHub Repository Setup**
- Create repo: `eth4nh4rdy/rant-circle`
- Initialize with `README.md`, `.gitignore` (Python), `LICENSE`
- Create `main` branch as default
- Clone locally to development machine
- Confirm remote is set correctly

**0.2 — Finalize Worksheet Specification**
- Confirm all page types, field labels, and layout decisions
- Confirm Listener Notes layout (sections vs. pages)
- Confirm Post-Class Reflection multi-entry structure
- Lock DOCX styling rules: fonts, margins, spacing, Primo branding, Rant Circle logo title treatment

**0.3 — Define `topics.yaml` Schema**
- Confirm fields: `slug`, `display_name`, `category`, `description`, `phrase_hints`
- `phrase_hints` are seed phrases passed to the LLM to guide Language Focus Card generation
- Confirm category list

**0.4 — Define `phrases.yaml` Schema**
- General empathy, advice, hedging, and pushback phrase clusters
- Used as fallback when no `--topic` is given or LLM call fails

**0.5 — Define Language Focus Card LLM Prompt Strategy**
- Determine what is passed to the LLM: topic slug, display name, description, phrase hints
- Define expected output schema (JSON with phrase categories)
- Define fallback behavior if LLM call fails or no topic provided

**0.6 — DOCX Style Specification**
- Font: Arial or equivalent
- Margins: 2cm all sides (A4)
- Header: Rant Circle logo title (text-based treatment — large, bold, branded) + session date + topic
- Footer: `Primo English | pf.kakao.com/_xivGxdX` centred, 9pt, grey
- Color accents: Primo blue (`#1F4E79`) for headers and section dividers
- Checkbox style: `□` Unicode — no form fields
- Page break strategy: Speaker Prep Sheets on new pages; Listener Notes sections use dividers only

**Phase 0 Deliverables**
- [ ] GitHub repo live at `eth4nh4rdy/rant-circle`
- [ ] Worksheet specification locked
- [ ] `topics.yaml` schema defined
- [ ] `phrases.yaml` schema defined
- [ ] LLM prompt strategy defined
- [ ] DOCX style specification locked

---

### Phase 1 — Project Scaffold

**Goal:** Establish the full project skeleton with all config files seeded and CLI stubbed.

#### Tasks

**1.1 — Directory Structure**
- Create all directories and placeholder files per the file structure above
- Add `output/.gitkeep`

**1.2 — `requirements.txt`**
- `python-docx`
- `anthropic` (or OpenAI-compatible SDK per LLM config)
- `python-dotenv`
- `pyyaml`
- `argparse` (stdlib — no install needed)

**1.3 — `topics.yaml` — Full Seed**
- All topics from the topic suggestion list above
- Full schema per 0.3 spec
- `phrase_hints` written for each topic

**1.4 — `phrases.yaml` — General Phrase Bank**
- Empathy openers
- Hedged advice
- Strong advice
- Pushback language
- Minimum 5 phrases per category

**1.5 — `.env.example`**
- `ANTHROPIC_API_KEY=your_key_here` (or equivalent)

**1.6 — `main.py` — CLI Stub**
- All flags defined and parsed
- Pipeline functions stubbed (no logic yet — just structure)
- Prints parsed args to confirm flag handling works

**Phase 1 Deliverables**
- [ ] Full directory structure in place
- [ ] All config YAML files seeded
- [ ] `.env.example` committed
- [ ] CLI stub runs without errors and prints parsed args
- [ ] Initial commit pushed to `eth4nh4rdy/rant-circle`

---

### Phase 2 — Static Page Generator

**Goal:** Generate all deterministic pages — everything except the Language Focus Card — without any LLM dependency.

#### Tasks

**2.1 — `formatter.py` — Document Skeleton**
- Initialize DOCX document with correct page size, margins, fonts
- Header function: Rant Circle logo title treatment + date + topic (or "General" if none)
- Footer function: Primo English branding

**2.2 — Warm Circle Check-In Page**
- One row per student (rows driven by `--students` flag)
- Name column + check-in sentence fill-in

**2.3 — Speaker Prep Sheet**
- Single page per ranter
- All fields per spec
- Checkbox row for support type
- Page break after each sheet

**2.4 — Listener Notes Sections**
- One section per ranter, rendered sequentially
- Fields per spec
- Section divider between entries (not page breaks)
- Listener Notes block introduced by a clear section header

**2.5 — Post-Class Reflection Page**
- Advice entries scale with `--ranters` flag
- All static fields per spec

**2.6 — Pipeline Integration**
- `main.py` calls formatter functions in correct page order
- Output file written to `./output/` with correct filename convention
- End-to-end test: `python main.py --ranters 2 --students 4` produces a valid DOCX

**Phase 2 Deliverables**
- [ ] All static pages generate correctly
- [ ] Output filename convention working
- [ ] Page count correct for multiple `--ranters` / `--students` combinations
- [ ] DOCX opens cleanly in Word and LibreOffice
- [ ] Commit pushed

---

### Phase 3 — Language Focus Card Generator

**Goal:** Generate a topic-tailored Language Focus Card via LLM call and render it as the first page of the DOCX.

#### Tasks

**3.1 — `generator.py` — LLM Prompt**
- Load topic data from `topics.yaml` using `--topic` slug
- Build prompt: inject topic display name, description, and phrase hints
- Request JSON output with 4 phrase categories: empathy / hedged advice / strong advice / pushback
- Minimum 3 phrases per category

**3.2 — API Call & Response Parsing**
- Call Anthropic API (claude-sonnet-4-6)
- Parse JSON response
- Strip markdown fences before parsing
- Validate: all 4 categories present, each has ≥ 3 phrases
- Retry once on validation failure

**3.3 — Fallback Logic**
- If `--topic` not provided: load general phrases from `phrases.yaml`
- If LLM call fails: load general phrases from `phrases.yaml` + log warning
- Fallback must never crash the pipeline

**3.4 — Language Focus Card Renderer**
- Rendered as Page 1 of the DOCX (before all other pages)
- Section header: "Language Focus Card" in Primo blue
- 4 phrase groups rendered with category labels
- Visually distinct from worksheet pages (lighter feel — reference card, not exercise page)

**3.5 — Integration & Test**
- `python main.py --ranters 2 --students 3 --topic work-hours` — topic-driven card
- `python main.py --ranters 2 --students 3` — fallback card
- `python main.py --ranters 2 --students 3 --topic bad-slug` — unknown slug fallback

**Phase 3 Deliverables**
- [ ] LLM call working with topic input
- [ ] JSON parsing and validation working
- [ ] Fallback logic confirmed (no topic, failed call, bad slug)
- [ ] Language Focus Card renders correctly as Page 1
- [ ] All three test commands pass
- [ ] Commit pushed

---

### Phase 4 — DOCX Formatting & Branding

**Goal:** Polish the full document to a classroom-ready, Primo-branded standard.

#### Tasks

**4.1 — Rant Circle Logo Title Treatment**
- "Rant Circle" rendered in large, bold, styled text as the document header
- Consistent across all page types
- No image dependency — text-based treatment using font weight, size, and colour
- Visually distinct from body text — functions as a logo-equivalent title

**4.2 — Primo English Footer**
- `Primo English | pf.kakao.com/_xivGxdX`
- Centred, 9pt, grey
- Page numbers right-aligned
- Applied to all pages

**4.3 — Full Layout Review**
- Spacing and whitespace reviewed for classroom printing
- Fill-in lines have correct length and spacing for handwriting
- Checkboxes render correctly (`□`)
- Section dividers are visually clear

**4.4 — Print Preview Check**
- Convert to PDF via LibreOffice headless
- Review all pages visually
- Confirm nothing bleeds off page, no orphaned headers, no layout breaks

**Phase 4 Deliverables**
- [ ] Rant Circle logo title consistent across all pages
- [ ] Primo English footer on all pages with page numbers
- [ ] Full layout review complete
- [ ] Print preview PDF generated and approved
- [ ] Commit pushed

---

### Phase 5 — Testing & Validation

**Goal:** Confirm the generator handles all realistic input combinations correctly and fails gracefully on edge cases.

#### Test Matrix

| Command | Expected Behaviour |
|---|---|
| `python main.py --ranters 1 --students 2` | 1 prep sheet, 1 listener section, 1 reflection entry |
| `python main.py --ranters 3 --students 3` | 3 prep sheets, 3 listener sections per listener, 3 reflection entries |
| `python main.py --ranters 5 --students 5` | 5 prep sheets, correct listener scaling |
| `python main.py --ranters 2 --students 4 --topic work-hours` | Topic-driven Language Focus Card |
| `python main.py --ranters 2 --students 3` | Fallback phrase card (no topic) |
| `python main.py --ranters 2 --students 3 --topic xyz` | Unknown slug — fallback, no crash |
| `python main.py --ranters 0 --students 3` | Graceful error — ranters must be ≥ 1 |
| `python main.py --ranters 3 --students 2` | Graceful error — students must be ≥ ranters |

#### Tasks

**5.1 — Run Full Test Matrix**
- All commands above executed
- Output DOCXs opened and reviewed
- Pass/fail logged

**5.2 — Edge Case Hardening**
- Fix any failures from 5.1
- Add input validation to `main.py` for nonsensical flag combinations

**5.3 — Windows 11 Manual Test**
- Open output DOCX in Microsoft Word on Windows 11
- Print preview check — A4, all pages correct
- Confirm Korean characters render correctly if any appear in topic display names

**Phase 5 Deliverables**
- [ ] Full test matrix passed
- [ ] Edge cases handled gracefully
- [ ] Windows 11 manual test confirmed
- [ ] No open bugs

---

### Phase 6 — Commit & Log

**Goal:** Clean close of the build. Full documentation and version control.

#### Tasks

**6.1 — Final Git Commit**
- All files staged and committed with a descriptive commit message
- Message must include: what was built, CLI interface summary, phase summary, known limitations if any

**6.2 — Project Log**
- Written in JSON format
- Includes: project state, completed phases, CLI reference, file structure, known issues, next steps
- Saved as `rant_circle_project_log_YYYYMMDD.json` in Primo English project knowledge

**6.3 — Master Roadmap Status Update**
- This file updated to reflect completed phases
- Open items and future enhancement ideas noted

**Phase 6 Deliverables**
- [ ] Final commit pushed to `eth4nh4rdy/rant-circle`
- [ ] Project log written and saved
- [ ] Master roadmap updated

---

## Future Enhancements (Post-V1)

These are deferred. Not in scope for the initial build.

- **PDF output option** — `--format pdf` flag for digital distribution
- **Korean UI option** — bilingual field labels on all pages
- **Student name pre-fill** — `--names "Jiyeon,Minsoo,Hyerim"` flag to pre-populate name fields
- **Session history log** — lightweight JSON log of past sessions (date, topic, ranters)
- **Scheduled generation** — cron job or Telegram trigger to auto-generate before class
- **Telegram delivery** — send generated DOCX directly to a student group chat

---

## Definition of Done

The Rant Circle Worksheet Generator is complete when:

- [ ] All 6 phases complete
- [ ] Generator produces a clean, print-ready DOCX for any valid flag combination
- [ ] Language Focus Card generates correctly for any seeded topic slug
- [ ] Fallback to general phrases confirmed working
- [ ] Windows 11 print preview approved
- [ ] Repository live at `eth4nh4rdy/rant-circle` with clean commit history
- [ ] Project log written

---

*Rant Circle Worksheet Generator — Master Roadmap v1.0*
*Primo English | primo-english.xyz*
