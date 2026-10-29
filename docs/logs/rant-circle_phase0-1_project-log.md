# Rant Circle — Project Log (Phases 0–2 in progress)

**Project:** Rant Circle Worksheet Generator
**Business:** Primo English (Seoul) — premium ESL coaching
**Repo:** `github.com/eth4nh4rdy/rant-circle` (public, branch `main`)
**Log date:** 2026-10-29
**Current position:** Phase 2 — Listener Notes pages done and pushed. Next: Post-Class Reflection page.

---

## 1. Read This First — How to Work With the User

These rules were established the hard way during this session. Follow them strictly.

- **This is the user's project. Do not assume.** Do not choose tools, libraries, providers, wording, layout, or architecture without checking first. Propose, then wait for confirmation.
- **Do not add anything the user hasn't reviewed.** No extra flags, fields, files, or features slipped in.
- **Do not regenerate whole documents to fix small errors.** Work forward. The user considers unnecessary regeneration a waste of tokens.
- **One task at a time.** Claude (in MODE: DEV) writes prompts; **Claude Code implements**. All Claude Code prompts go in a single copy-paste code block.
- **Ask focused questions, not obvious ones.** The user gets frustrated by questions with obvious answers (e.g. "should the name line be on every page?" — obviously first page only). Ask only where a real decision exists.
- **Verify Claude Code's self-reports.** Ask the user to check the actual `.docx` output (they paste page text back). A previous Claude Code session wandered outside the repo and reported success on a broken file.
- **The user only uses LibreOffice** (not Microsoft Word) to view output.

### Git rules (strict)
- **Never use `git add .`** — always name files explicitly: `git add formatter.py`
- Always run `git status` after adding and confirm `.env` is NOT staged before committing.
- **Commit messages: one single-line `git commit -m "..."` with NO double quotes inside the message.** Multi-line messages and inner double quotes broke PowerShell. Keep it clean, detailed, one line.
- Provide add/commit/push in the format the user asks for (often one code block).
- **Before working on a different machine, `git pull origin main` first.** The Windows machine once fell behind origin and Claude Code built on a stale `formatter.py`, losing work — recovered via `git stash`, pull, and redo.

### Machines / shells
- **Windows 11 main rig** — PowerShell. `C:\Users\smeefer\primo_english\rant-circle`. No `printf`, no heredocs.
- **CachyOS laptop** — fish shell. `~/primo_english/rant-circle`. No bash heredocs (`<<`).
- Give shell commands appropriate to whichever machine the user is on.

---

## 2. Program Concept

Rant Circle is a flexible 60-minute group English class (Primo English). Students rant about real-life problems or observations in English; other students listen, ask follow-ups, and give advice.

- **Flexibility is a goal, not a rule.** Not everyone has to rant. Some students may only give advice that day. Speaking order may be decided by dice, volunteering, or the teacher.
- Teacher is a facilitator, not a counselor. Topics are real-life, not crisis-level.
- Theme across the worksheet is a **meal arc**: cook the rant → serve the advice → dessert (reflection).

---

## 3. Major Decisions That DIFFER From the Master Roadmap

The master roadmap (`rant_circle_master_roadmap.md`, stored locally in untracked `roadmaps/`) was **not regenerated** by user's choice. These corrections override it:

| Topic | Master roadmap says | Actual decision |
|---|---|---|
| Output model | One shared group packet per session | **One run = one individual student's worksheet** |
| `--ranters` | Number of students ranting | **Number of Listener Notes pages to print** on this one worksheet |
| `--students` | Included (CLI, filename `R{n}S{n}`) | **Removed entirely. Never add it.** |
| `--topic` | Session topic | **This one student's own rant topic** (single value). Each student picks their own topic. |
| Warm Circle Check-In page | Separate page with group table | **Cut entirely.** Replaced by warm-up content on page 1 |
| LLM provider | Anthropic SDK / claude-sonnet | **OpenRouter via `requests` (REST). Model TBD.** No `anthropic` package. |
| Config file location | Repo root | **`config/topics.yaml`, `config/phrases.yaml`** |
| `phrases.yaml` categories | 4 | **6**: empathy, hedged_advice, strong_advice, pushback, agreement, exclamation — plus `checkin_questions` pool |
| Margins | 2cm | **python-docx default** |
| Footer | Primo English + Kakao link | **`www.primo-english.xyz` only, no Kakao** |
| Logo | Text logo treatment in Phase 4 | **Deferred entirely** until program works. Plain text title for now. Mascot also planned later. |
| Colour | Primo blue `#1F4E79` | **Deep Biosphere palette** — `space-indigo #282C45` for accents only; body text black; white background |
| Listener Notes layout | Continuous sections with dividers | **Each section on its own page**, titled, **no dividers** |
| Language Focus Card | Session topic phrases only | Tailored to the **student's own topic**; same LLM call also generates **2 topic-primer warm-up questions** for page 1 |

---

## 4. Locked Specifications

### CLI (main.py)
```
python main.py --ranters 3 --topic workhours --date 2026-09-16 --out ./output
```
- `--ranters` int, required, ≥1 (validated, exits with clear error)
- `--topic` str, optional (slug from `config/topics.yaml`)
- `--date` str, optional, defaults to today, YYYY-MM-DD
- `--out` str, optional, defaults to `./output`
- Currently a **stub only** — parses and prints args. Not yet wired to `formatter.py`.

### DOCX style
- A4, python-docx default margins
- Font: **Arial** everywhere (may change later to a font usable in LibreOffice on Windows + Linux)
- Body text: **14pt**, black
- Main title "Rant Circle": **34pt bold space-indigo** (size reserves space for future logo)
- Page titles: **26pt bold space-indigo**
- Footer (true section footer, repeats): `www.primo-english.xyz` centred, **10pt** grey (user changed from 9pt) + right-aligned auto page number
- Checkboxes: Unicode `□`, no form fields
- Header is **manually inserted body content** (not a true docx header), because content varies per page

### `config/topics.yaml`
Schema: `slug`, `display_name`, `category`, `description`, `phrase_hints` (2 per topic). Slugs one word ideal, two words max.
16 topics: `workhours`, `badboss`, `coworkers`, `friendship`, `burnout`, `laws`, `prices`, `stocks`, `restaurants`, `weather`, `general`, `family`, `health`, `housing`, `military`, `exams`, `nunchi`. (User compiled the final file; more topics to be added later.)

### `config/phrases.yaml`
- 6 phrase categories, ≥5 each (starter set). User will heavily expand with slang and less AI-sounding entries.
- `checkin_questions`: 10 light questions, one chosen randomly per run for page 1.
- **Must be opened with `encoding="utf-8"`** (fixed bug — cp1252 on Windows garbled em dashes).

### `.env` / `.gitignore`
- `.env.example`: `OPENROUTER_API_KEY=your_key_here`
- `.gitignore`: `.env`, `__pycache__/`, `*.pyc`, `*.pyo`, `.venv/`, `venv/`, `output/`, `.DS_Store`, `Thumbs.db`
- `roadmaps/` exists locally and is untracked. **User decided NOT to add `/roadmaps` or `/logs` to `.gitignore`** — just never stage them.

### requirements.txt
`python-docx`, `python-dotenv`, `pyyaml`, `requests` (unpinned)

---

## 5. Worksheet Page Structure — Current State

### Page 1 — Cover + Warm-Up (DONE)
- `add_header(document, name_field=True, date, topic)`: "Rant Circle" 34pt, `Name: ___________________` (page 1 only), `Date: September 16, 2026`, `Topic: <display name>` (or "General")
- `add_page1_content(document, topic_slug)`: bold indigo "Warm-Up:" label + random `checkin_questions` entry; then two italic placeholders `[Topic-primer question 1 — generated in Phase 3]` / `[... 2 ...]`
- **No answer lines** for warm-up questions (answered aloud)

### Page 2 — Speaker Prep Sheet (DONE)
- `add_speaker_prep_sheet(document)`, page break first
- Title: **"Time to Start Cooking...a Rant!"** (26pt)
- Prompts with handwriting space: "What's on your mind?" / "The main feeling behind it" / "Have you already said or done anything about it?"
- "What kind of feedback would you like?" — borderless 2×2 grid: □ Practical advice, □ A reality check, □ Nothing. I just want to vent., □ Any of the above
- "Maybe useful words" — 3 short blanks side by side
- Thought bubbles were tried (DrawingML) and **removed** — rendered badly. No bubbles, no decorative lines.

### Pages 3+ — Listener Notes (DONE, pushed)
- `add_listener_notes(document, ranters)` — loop `ranters` times, **page break before every section**
- First title: **"Time to Serve Up Some Advice"**; subsequent: **"Time to Dish Up More Advice"** (26pt)
- **No "Listening Notes"/"Listener Notes" heading. No dividers.**
- Fields: Speaker name / Topic / Notes / Follow-up questions / My advice / One thing they said that resonated with me
- User manually removed "(use a phrase from the Language Focus Card)" from "My advice:"

### Final Page — Post-Class Reflection (NEXT — not built)
Decisions so far:
- **New page**
- **Take-home** (filled in after class)
- Dessert-themed title — **NOT locked yet**. Proposed favourite: "Save Room for Dessert". Others offered: "Time for Dessert: Reflections", "The Sweet Leftovers", "One Last Bite", "A Little Something Sweet". **Confirm with user.**
- "Advice I appreciated today" — **one entry per ranter** (scales with `--ranters`), each with **`From: _____________`** plus space for the advice (user wants to see how it looks)
- Other fields (from original spec — confirm wording with user before building): A phrase I used today that I'm proud of / A phrase I heard that I want to use again / Something I want to say better next time / My topic for next session (if I want to go again)

### Language Focus Card (Phase 3 — not built)
- Tailored to this student's topic; 6 categories, **minimum 3 phrases each** (provisional — revisit after seeing a rendered page, 18 phrases may crowd one page)
- Fallback to `phrases.yaml` if no topic, unknown slug, or LLM failure — never crash
- **Page placement is an OPEN question.** Earlier proposed order was cover → Language Focus Card → Speaker Prep → Listener Notes → Reflection, but Speaker Prep was built as page 2. Ask the user where the card goes.

---

## 6. Code State (`formatter.py`)

Functions present: `create_document`, `add_header`, `add_footer`, `add_section_divider` (now unused by Listener Notes; contains a non-breaking-space fix so the border renders), `add_page1_content`, `add_speaker_prep_sheet`, `add_listener_notes`, plus private helpers (e.g. `_set_paragraph_bottom_border`, `_add_open_prompt`).

Other fixes in code:
- Date formatting uses `%d` + `.replace(" 0", " ")` instead of Linux-only `%-d` (crashed on Windows)
- YAML read with `encoding="utf-8"`

`__main__` test block builds: `create_document → add_footer → add_header → add_page1_content → add_speaker_prep_sheet → add_listener_notes(ranters=3)` → `output/skeleton_test.docx`.

`generator.py` is empty (Phase 3).

---

## 7. Commit History (main)

```
(latest)  Phase 2: Listener Notes pages (pushed 2026-10-29; hash not recorded)
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
| 2 — Static pages | **In progress**: skeleton, page 1, page 2, Listener Notes done. Reflection page + pipeline integration remain |
| 3 — Language Focus Card + topic-primer questions (OpenRouter) | Not started |
| 4 — Formatting & branding (logo deferred) | Not started |
| 5 — Testing & validation | Not started |
| 6 — Commit & log | Ongoing per task |

---

## 9. What Happens Next

1. **Confirm the dessert title** and the exact Reflection field wording with the user.
2. Write a Claude Code prompt for `add_post_class_reflection(document, ranters)` (new page, title 26pt indigo, `From: ___` + advice entries × ranters, remaining fields). Add it to the `__main__` test block.
3. User checks `skeleton_test.docx` in LibreOffice and pastes page text. Fix as needed.
4. Commit (explicit `git add formatter.py`, `git status`, single-line `-m` message, no inner double quotes) and push.
5. **Task 2.6 — Pipeline integration:** wire `main.py` CLI to `formatter.py` — topic slug → `display_name` lookup from `topics.yaml`, `--ranters` → Listener Notes pages + Reflection entries, `--date`, `--out`. Confirm the output filename convention with the user (roadmap had `rant_circle_YYYYMMDD_R{n}.docx`; `S{n}` must not be used). Decide with the user whether the `__main__` test block in `formatter.py` stays.
6. Then **Phase 3**: OpenRouter call in `generator.py` for the Language Focus Card + 2 topic-primer questions; settle card placement; fallback logic. Model to be chosen by user.

### Deferred / later
- Expand `topics.yaml` and `phrases.yaml` (user will do much of this)
- Font change, Rant Circle logo, mascot meme character
- Future enhancements from roadmap (PDF output, bilingual labels, name pre-fill, Telegram delivery) — not in scope
