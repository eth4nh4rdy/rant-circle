# Rant Circle — Project Log (Phases 0–2 complete)

**Project:** Rant Circle Worksheet Generator
**Business:** Primo English (Seoul) — premium ESL coaching
**Repo:** `github.com/eth4nh4rdy/rant-circle` (public, branch `main`)
**Log date:** 2026-11-04
**Current position:** Phase 2 COMPLETE and pushed. Next: Phase 3 (OpenRouter Language Focus Card + topic-primer questions).
**Supersedes:** `rant-circle_phase0-1_project-log.md` (that log is now historical). Where this log and `rant_circle_master_roadmap.md` conflict, **this log wins**.

---

## 1. Read This First — How to Work With the User

These rules were established the hard way. Follow them strictly.

- **This is the user's project. Do not assume.** Do not choose tools, libraries, providers, wording, layout, or architecture without checking first. Propose, then wait for confirmation.
- **Do not add anything the user hasn't reviewed.** No extra flags, fields, files, defaults, or features slipped in. (Claude Code has a habit of adding small things, e.g. a `date=None` default; always flag these.)
- **Do not regenerate whole documents to fix small errors.** Work forward. Unnecessary regeneration wastes tokens.
- **One task at a time.** Claude (MODE: DEV) writes prompts; **Claude Code implements**. Every Claude Code prompt goes in a single copy-paste code block.
- **Ask focused questions, not obvious ones.** Ask only where a real decision exists.
- **Verify Claude Code's self-reports.** The user opens the actual `.docx` and pastes page text back. A previous Claude Code session wandered outside the repo and reported success on a broken file.
- **The user only uses LibreOffice** (not Microsoft Word) to view output.
- **Be precise when scoping a correction.** In Task 2.6 the user said "no hyphens in the date" meaning the *filename only*; Claude Code changed the `--date` input format too and had to be corrected. State explicitly what a change does NOT touch.
- **Claude Code pre-checks:** a "stop if the latest commit isn't X" check is too strict, because docs-only commits can land on top. Instead have Claude Code run `git show --stat <hash>` and continue if only docs/log files are touched.

### Git rules (strict)
- **Never use `git add .`** — name files explicitly: `git add main.py formatter.py`
- Always run `git status` after adding and confirm `.env` (and any untracked file such as `CLAUDE.md`) is NOT staged before committing.
- **Commit messages: one single-line `git commit -m "..."` with NO double quotes inside the message.** Multi-line messages and inner double quotes broke PowerShell. Keep it clean, detailed, one line.
- **Before working on a different machine, `git pull origin main` first.** The Windows machine once fell behind origin and Claude Code built on a stale `formatter.py`, losing work.
- If a push fails with `remote: Internal Server Error`, it is a GitHub-side outage: the local commit is safe. Retry later; never force-push or redo the commit. (This happened on the Task 2.6 push; the retry succeeded.)
- Claude Code is told never to run `git add`, `commit` or `push`. The user does these.

### Machines / shells
- **Windows 11 main rig** — PowerShell. `C:\Users\smeefer\primo_english\rant-circle`. No `printf`, no heredocs.
- **CachyOS laptop** — fish shell. `~/primo_english/rant-circle` (`/home/smeefer/primo_english/rant-circle`). No bash heredocs (`<<`).
- Give shell commands appropriate to whichever machine the user is on. The user states the machine; Task 2.5/2.6 were done on the CachyOS laptop.

---

## 2. Program Concept

Rant Circle is a flexible 60-minute group English class (Primo English). Students rant about real-life problems or observations in English; other students listen, ask follow-ups, and give advice.

- **Flexibility is a goal, not a rule.** Not everyone has to rant. Some students may only give advice that day. Speaking order may be decided by dice, volunteering, or the teacher.
- Teacher is a facilitator, not a counselor. Topics are real-life, not crisis-level.
- Theme across the worksheet is a **meal arc**: cook the rant (Speaker Prep) → serve the advice (Listener Notes) → dessert (Reflection).
- **Output model:** one run = one individual student's worksheet. For multiple students the user prints the same file several times.

---

## 3. Decisions That DIFFER From the Master Roadmap

The master roadmap was **not regenerated** by user's choice. These corrections override it:

| Topic | Master roadmap says | Actual decision |
|---|---|---|
| Output model | One shared group packet per session | **One run = one individual student's worksheet** |
| `--ranters` | Number of students ranting | **Number of Listener Notes pages (and Reflection advice entries)** on this one worksheet |
| `--students` | Included (CLI, filename `R{n}S{n}`) | **Removed entirely. Never add it.** |
| `--topic` | Session topic | **This one student's own rant topic** (single slug). Each student picks their own topic. |
| Output filename | `rant_circle_YYYYMMDD_R{n}S{n}.docx` | **`rant-circle_<slug>_<YYYYMMDD>.docx`**, or `rant-circle_no-topic_<YYYYMMDD>.docx` with no topic. Auto-numbered `_2`, `_3` on collision. |
| Warm Circle Check-In page | Separate page with group table | **Cut entirely.** Replaced by warm-up content on page 1 |
| LLM provider | Anthropic SDK / claude-sonnet | **OpenRouter via `requests` (REST). Model TBD (user chooses).** No `anthropic` package. |
| Config file location | Repo root | **`config/topics.yaml`, `config/phrases.yaml`** |
| `phrases.yaml` categories | 4 | **6**: empathy, hedged_advice, strong_advice, pushback, agreement, exclamation — plus `checkin_questions` pool |
| Margins | 2cm | **python-docx default** |
| Footer | Primo English + Kakao link | **`www.primo-english.xyz` only, no Kakao** |
| Logo | Text logo treatment in Phase 4 | **Deferred entirely** until program works. Plain text title for now. Mascot also planned later. |
| Colour | Primo blue `#1F4E79` | **Deep Biosphere palette** — `space-indigo #282C45` for accents only; body text black; white background |
| Listener Notes layout | Continuous sections with dividers | **Each section on its own page**, titled, **no dividers** |
| Language Focus Card | Session topic phrases only | Tailored to the **student's own topic**; same LLM call also generates **2 topic-primer warm-up questions** for page 1 |
| Reflection page | "Session date" + static fields | Title "Save Room for Dessert", date line shown, "phrase **or word**" wording (see section 5) |
| Repo docs location | `roadmaps/` untracked | Roadmap and logs are **tracked under `docs/`** (commit `9a17a8f`): `docs/roadmaps/rant_circle_master_roadmap.md`, `docs/logs/rant-circle_phase0-1_project-log.md` |

---

## 4. Locked Specifications

### CLI (`main.py`) — now fully wired
```
python main.py --ranters 3 --topic workhours --date 2026-09-16 --out ./output
```
- `--ranters` int, **required**, ≥ 1 (validated; clear error, exit 1)
- `--topic` str, optional — slug from `config/topics.yaml`
- `--date` str, optional, **entered and validated as `YYYY-MM-DD`** (must be a real calendar date), defaults to today (`date.today().isoformat()`)
- `--out` str, optional, defaults to `./output`; created only after all validation passes
- **Never add** `--students` or any other flag without the user's approval.

Behaviour (verified by Claude Code and by the user's own check):
1. Validate `--ranters` and `--date`. Bad date → error stating `YYYY-MM-DD` with example `2026-09-16`, exit 1, nothing generated. (`20260916` and `16-09-2026` both rejected.)
2. Load `config/topics.yaml` (`encoding="utf-8"`). Unknown slug → error to stderr naming the bad slug and listing all valid slugs (sorted), exit 1, **before** the output directory or document is created. No topic → header shows "General", filename uses `no-topic`.
3. Build order: `create_document → add_footer → add_header → add_page1_content → add_speaker_prep_sheet → add_listener_notes(ranters) → add_post_class_reflection(ranters, date)`. The same validated `YYYY-MM-DD` string goes to `add_header` and `add_post_class_reflection`.
4. Filename: `rant-circle_<slug>_<YYYYMMDD>.docx` (hyphens stripped from the validated date **for the filename only**). Never overwrites: file is opened in exclusive-create mode; first file has no suffix, then `_2`, `_3` before the extension (e.g. `rant-circle_workhours_20260916_2.docx`).
5. On success prints one line: the path written. All errors go to stderr.

Verified filenames from testing: `rant-circle_workhours_20260916.docx`, `..._2`, `..._3`, `rant-circle_no-topic_20260916.docx`, `rant-circle_no-topic_20261104.docx` (no `--date`).

The `__main__` test block in `formatter.py` was **removed** (user: no test versions in the scripts). `main.py` is now the way to test.

### DOCX style
- A4, python-docx default margins
- Font: **Arial** everywhere (may change later to a font usable in LibreOffice on Windows + Linux)
- Body text: **14pt**, black
- Main title "Rant Circle": **34pt bold space-indigo** (size reserves space for future logo)
- Page titles: **26pt bold space-indigo**
- Footer (true section footer, repeats): `www.primo-english.xyz` centred, **10pt** grey + right-aligned auto page number
- Checkboxes: Unicode `□`, no form fields
- Header is **manually inserted body content** (not a true docx header), because content varies per page

### `config/topics.yaml`
Schema: `slug`, `display_name`, `category`, `description`, `phrase_hints` (2 per topic). Slugs one word ideal, two words max.
**17 topics** (the Phase 0–1 log said 16 but listed 17; the code confirms 17): `workhours`, `badboss`, `coworkers`, `friendship`, `burnout`, `laws`, `prices`, `stocks`, `restaurants`, `weather`, `general`, `family`, `health`, `housing`, `military`, `exams`, `nunchi`. More topics to be added later by the user.

### `config/phrases.yaml`
- 6 phrase categories, ≥5 each (starter set). User will heavily expand with slang and less AI-sounding entries.
- `checkin_questions`: 10 light questions, one chosen randomly per run for page 1 (so page 1 differs run to run).
- **Must be opened with `encoding="utf-8"`** (fixed bug — cp1252 on Windows garbled em dashes).

### `.env` / `.gitignore`
- `.env.example`: `OPENROUTER_API_KEY=your_key_here`
- `.gitignore`: `.env`, `__pycache__/`, `*.pyc`, `*.pyo`, `.venv/`, `venv/`, `output/`, `.DS_Store`, `Thumbs.db`
- `output/` is git-ignored. Never stage `.env` or `CLAUDE.md`.

### requirements.txt
`python-docx`, `python-dotenv`, `pyyaml`, `requests` (unpinned)

---

## 5. Worksheet Page Structure — Current State (all built)

A 3-ranter worksheet is **6 pages**: page 1, Speaker Prep, 3 × Listener Notes, Reflection (verified by headless LibreOffice PDF conversion).

### Page 1 — Cover + Warm-Up (DONE)
- `add_header(document, name_field=True, date, topic)`: "Rant Circle" 34pt, `Name: ___________________` (page 1 only), `Date: September 16, 2026`, `Topic: <display name>` (or "General")
- `add_page1_content(document, topic_slug)`: bold indigo "Warm-Up:" label + random `checkin_questions` entry; then two italic placeholders `[Topic-primer question 1 — generated in Phase 3]` / `[... 2 ...]`
- **No answer lines** for warm-up questions (answered aloud)
- Note: `topic_slug` is accepted but currently unused; Phase 3 will use it.

### Page 2 — Speaker Prep Sheet (DONE)
- `add_speaker_prep_sheet(document)`, page break first
- Title: **"Time to Start Cooking...a Rant!"** (26pt)
- Prompts with handwriting space: "What's on your mind?" / "The main feeling behind it" / "Have you already said or done anything about it?"
- "What kind of feedback would you like?" — borderless 2×2 grid: □ Practical advice, □ A reality check, □ Nothing. I just want to vent., □ Any of the above
- "Maybe useful words" — 3 short blanks side by side
- Thought bubbles were tried (DrawingML) and **removed** — rendered badly. No bubbles, no decorative lines.

### Pages 3+ — Listener Notes (DONE)
- `add_listener_notes(document, ranters)` — loop `ranters` times, **page break before every section**
- First title: **"Time to Serve Up Some Advice"**; subsequent: **"Time to Dish Up More Advice"** (26pt)
- **No "Listening Notes"/"Listener Notes" heading. No dividers.**
- Fields: Speaker name / Topic / Notes / Follow-up questions / My advice / One thing they said that resonated with me
- User manually removed "(use a phrase from the Language Focus Card)" from "My advice:"

### Final Page — Post-Class Reflection (DONE, commit `bd3e776`)
`add_post_class_reflection(document, ranters, date=None)` — new page, take-home. In order:
1. Title: **"Save Room for Dessert"** (26pt bold space-indigo)
2. `Date: <formatted date>` (same format as `add_header`, e.g. "September 16, 2026"; no `%-d`)
3. Bold indigo label: **"Advice I appreciated today:"**
4. One entry per ranter: `From: _____________` + handwriting space (2 blank lines each). No numbering, no dividers.
5. Four prompts, 1 blank line each, via `_add_open_prompt`:
   - A phrase or word I used today that I'm proud of:
   - A phrase or word I heard that I want to use again:
   - Something I want to say better next time:
   - My topic for next session (if I want to go again):
- Fits one page for 1–4 ranters; **5 ranters spills to a second page** (user has not asked to fix this).
- Claude Code added a `date=None` default (falls back to today, like `add_header`) that the user did not specify. Left in place; offered a one-line fix to make `date` required. Not yet decided.
- Handwriting space is tight (1 blank line per prompt at 14pt). The user was asked to judge this in LibreOffice; revisit in Phase 4 layout review if it is too small.

### Language Focus Card (Phase 3 — not built)
- Tailored to this student's topic; 6 categories, **minimum 3 phrases each** (provisional — revisit after seeing a rendered page, 18 phrases may crowd one page)
- Fallback to `phrases.yaml` if no topic, unknown slug, or LLM failure — never crash. (Note: an unknown slug at the CLI is now a hard error handled in `main.py`; the card fallback covers LLM failure and the no-topic case.)
- **Page placement is an OPEN question.** Earlier proposed order was cover → Language Focus Card → Speaker Prep → Listener Notes → Reflection, but Speaker Prep was built as page 2. Ask the user where the card goes.

---

## 6. Code State

### `formatter.py`
Functions: `create_document`, `add_header`, `add_footer`, `add_section_divider`, `add_page1_content`, `add_speaker_prep_sheet`, `add_listener_notes`, `add_post_class_reflection`, plus private helpers (`_set_paragraph_bottom_border`, `_add_open_prompt`, and others). **No `__main__` block.**
- `add_section_divider` is **no longer called anywhere** (dead code). Contains a non-breaking-space fix so the border renders. **Open decision:** delete in a small separate cleanup task (assistant's lean) or keep.
- `add_page1_content` opens `config/phrases.yaml` **relative to the current directory**, so `main.py` must be run from the repo root. `main.py` itself locates `topics.yaml` relative to its own location. User has not asked to change this; candidate for Phase 4/5 hardening.
- Date formatting uses `%d` + `.replace(" 0", " ")` instead of Linux-only `%-d` (crashed on Windows).

### `main.py`
Fully wired per section 4. Uses `os.path`/`pathlib` and utf-8 so it works on Windows 11 and Linux.

### `generator.py`
Empty (Phase 3).

### Untracked / housekeeping
- `CLAUDE.md` — created by an earlier Claude Code session, **untracked and stale** (still says `main.py` isn't wired to the formatter). **Open decision:** keep in repo (and update), git-ignore, or delete. Do not stage it unless the user says so.
- Local `output/` may hold old test files (`skeleton_test.docx`, `_2`/`_3` copies); git-ignored, safe to delete.

---

## 7. Commit History (main)

```
d599a19   Phase 2 Task 2.6: wire main.py to formatter.py (topic validation, YYYY-MM-DD date check, auto-numbered output, test block removed)  [pushed 2026-11-04 after one GitHub 500 retry]
bd3e776   Phase 2 Task 2.5: Post-Class Reflection page
9a17a8f   Putting the master roadmap and first project log in the repo (docs only)
dcbf4ff   Phase 2: Listener Notes pages
20e824b   Phase 2: Speaker Prep Sheet (page 2)
d343008   Phase 2 Task 2.2: Page 1 warm-up content
0822f91   Phase 2 Task 2.1: document skeleton for formatter.py
9b1f281   Merge branch 'main' (pulled GitHub-generated LICENSE)
b7b67f5   Phase 1 complete: project scaffold
aac825d   Initial commit (LICENSE, created by GitHub)
```

---

## 8. Phase Status

| Phase | Status |
|---|---|
| 0 — Design, spec, repo setup | Done |
| 1 — Scaffold | Done |
| 2 — Static pages + pipeline | **Done** (2.1–2.6 all committed and pushed) |
| 3 — Language Focus Card + topic-primer questions (OpenRouter) | **Next — not started** |
| 4 — Formatting & branding (logo deferred) | Not started |
| 5 — Testing & validation | Not started |
| 6 — Commit & log | Ongoing per task |

---

## 9. What Happens Next — Phase 3

Before any Claude Code prompt, settle these with the user (real decisions, ask them):
1. **OpenRouter model** — user chooses. Do not pick one.
2. **Language Focus Card placement** — see section 5 (open question).
3. **Phrases per category** — provisional minimum 3 × 6 categories; confirm after seeing a rendered card.
4. **Prompt/response design** — what is sent (display name, description, `phrase_hints`), the JSON output schema (6 phrase categories + 2 topic-primer questions), JSON parsing/validation, retry-once on validation failure. Propose, then wait for confirmation.
5. **Fallback behaviour** — no topic or LLM failure → phrases from `phrases.yaml`, log a warning, never crash. Decide what the topic-primer placeholders show in fallback (e.g. generic questions vs. blank).
6. `OPENROUTER_API_KEY` is read from `.env` via `python-dotenv`; REST via `requests`; no SDK. All prompts/workflows must work with Claude or Hermes as the implementer.

Per DEV workflow: research → plan (a Phase 3 sub-roadmap if the user wants one) → implement → test → merge → commit/log.

### Open housekeeping decisions (none blocking)
- `CLAUDE.md`: keep / ignore / delete
- `add_section_divider`: delete / keep
- `date` default on `add_post_class_reflection`: keep `None` default or make required
- Reflection page spill at 5 ranters: leave or fix
- Working-directory dependence of `add_page1_content`: leave or fix in Phase 4/5

### Deferred / later
- Expand `topics.yaml` and `phrases.yaml` (user will do much of this)
- Font change, Rant Circle logo, mascot meme character
- Future enhancements from roadmap (PDF output, bilingual labels, name pre-fill, Telegram delivery) — not in scope
