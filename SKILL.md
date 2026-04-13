---
name: distill-my-mentor
description: |
  Distill your academic mentor into an AI Skill that guides your research, revises your papers, and advises on direction in their style.
  Import emails, paper annotations, chat logs, literature PDFs, and your own descriptions
  to generate a digital mentor Skill that thinks, reviews, and advises like them.
  Trigger: /distill-my-mentor — create a new mentor Skill.
  Also trigger when the user says "distill my mentor", "create mentor skill", "distill my advisor",
  "蒸馏导师", "创建导师", or wants to capture an academic mentor's style.
---

# Mentor Skill Creator

Distill your mentor into an AI Skill. Use their voice to revise your papers, set direction, and do research.

Your advisor graduated, retired, or moved on — but the things they said to you:
"There's a fundamental problem with your experimental design." "Your logical chain is broken." "Get the literature review solid first."
Those voices don't have to disappear.

---

## Language

Detect the user's language from their first message and respond in the same language throughout.
Support both Chinese and English. Many academic mentors in China speak Chinese daily but write papers in English — the generated Skill should reflect this bilingual reality.

---

## Commands

| Command | Action |
|---------|--------|
| `/distill-my-mentor` | Create a new mentor Skill |
| `/list-mentors` | List all generated mentor Skills |
| `/mentor-rollback {slug} {version}` | Rollback to a previous version |
| `/delete-mentor {slug}` | Delete a mentor Skill |

Generated mentor Skills support these sub-commands:

| Command | Action |
|---------|--------|
| `/{slug}` | Full conversation mode (daily chat) |
| `/{slug}-review` | Annotation-style paper review |
| `/{slug}-rewrite` | Demonstration rewrite in mentor's style |
| `/{slug}-advise` | Research direction guidance + structured outline |
| `/{slug}-guidance` | Guidance memory only |
| `/{slug}-style` | Academic style only |

---

## Base directory

Skill files are written to `./mentors/{slug}/` (relative to this skill's directory).

> **Runtime note**: All tool commands in this Skill use `${CLAUDE_SKILL_DIR}` to reference the skill's own directory. When executing bash commands, Claude should resolve this variable to the actual path of this skill file's directory. For example:
> ```bash
> export CLAUDE_SKILL_DIR="/path/to/distill-my-mentor"  # set once at start of session
> ```
> In Claude Code, `CLAUDE_SKILL_DIR` is typically set automatically. In other environments, set it manually before running any tool commands.

---

## Workflow: /distill-my-mentor

### Phase 0 — Online Research (automatic, no user confirmation needed)

After the user provides the mentor's **name** and **institution**, immediately conduct automated web research WITHOUT asking for permission. Execute these searches in Claude Code terminal:

1. `web_search("{name} {institution} research")`
2. `web_search("{name} Google Scholar publications")`
3. `web_search("{name} {institution} professor page")`
4. `web_search("{name} interview OR keynote OR invited talk")`
5. `web_search("{name} ResearchGate OR ORCID")`

For each promising result, use `web_fetch` to retrieve the full page content.

Then apply `${CLAUDE_SKILL_DIR}/prompts/profile_analyzer.md` to process the raw search results into a structured `baseline_profile.md`. This becomes the L0 foundation — user data will enrich it later.

Save to `mentors/{slug}/knowledge/baseline_profile.md`.

Show the user a brief summary of what was found and proceed to Phase 1.

### Phase 1 — Intake (interactive)

Read `${CLAUDE_SKILL_DIR}/prompts/intake.md` for the full question sequence. Ask only 3 questions at a time, all fields skippable:

**Block 1 — Basic info** (pre-filled from Phase 0 where possible):
1. Mentor's name/alias (e.g. "Prof. Zhang", "Dr. Smith", "my advisor")
2. Research field and direction
3. Relationship duration and stage (e.g. "Master's, 3 years", "PhD year 1-3", "one-year visiting student")

**Block 2 — Style portrait** (plain language):
4. "Describe their mentoring style in a few sentences."
   Suggest tags: Strict / Hands-off / Push-oriented / Laissez-faire / Detail-obsessed / Big-picture / Socratic / Direct / Affirm-then-critique / Silent-pressure …

**Block 3 — Data import** (all optional):
5. Chat logs? (WeChat/QQ/DingTalk/Feishu)
6. Emails? (.eml / .mbox / .msg files)
7. Paper annotations? (annotated PDF / Word with track changes / reviewer response letters)
8. Literature folder? (a directory of PDF papers — mentor's publications and/or recommended readings)
9. Social media / photos?
10. Nothing? Just tell me about them — pure description works too.

### Phase 2 — Data Processing

For each data source provided, run the appropriate parser:

```
# Chat logs
python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py --file {path} --target "{name}" --output /tmp/chat_out.txt
python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py --file {path} --target "{name}" --output /tmp/qq_out.txt

# Emails
python3 ${CLAUDE_SKILL_DIR}/tools/email_parser.py --dir {path} --mentor-email "{email}" --output /tmp/email_out.txt

# Paper annotations
python3 ${CLAUDE_SKILL_DIR}/tools/paper_comment_parser.py --file {path} --output /tmp/comments_out.txt

# Literature folder
python3 ${CLAUDE_SKILL_DIR}/tools/literature_parser.py --dir {path} --mentor-name "{name}" --output /tmp/lit_analysis.txt

# Social media
python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py --file {path} --platform {platform} --target "{name}" --output /tmp/social_out.txt

# Photos
python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py --dir {path} --output /tmp/photo_timeline.txt
```

Then Read the output files to collect all raw materials.

### Phase 3 — Analysis

Combine all collected materials and user descriptions. Analyze along three tracks:

1. **Guidance analysis**: Read `${CLAUDE_SKILL_DIR}/prompts/guidance_analyzer.md`. Extract guidance memories — how the mentor reviews papers, runs meetings, gives feedback, handles student mistakes, pushes progress.

2. **Style analysis**: Read `${CLAUDE_SKILL_DIR}/prompts/style_analyzer.md`. Extract the 5-layer academic style structure using the tag translation table.

3. **Literature analysis**: Read `${CLAUDE_SKILL_DIR}/prompts/literature_analyzer.md`. From the literature folder analysis, extract academic fingerprint — research trajectory, writing patterns, methodological preferences, high-frequency terminology.

### Phase 4 — Generation

Read the builder templates and generate each component:

1. `${CLAUDE_SKILL_DIR}/prompts/guidance_builder.md` → `guidance.md`
2. `${CLAUDE_SKILL_DIR}/prompts/style_builder.md` → `style.md` (5-layer structure)
3. `${CLAUDE_SKILL_DIR}/prompts/thinking_framework_builder.md` → `thinking_framework.md`

Show the user a summary (5-8 lines each):

```
Mentoring Memory Summary:
- Relationship duration: {duration}
- Key mentoring scenarios: {N}
- Paper revision style: {xxx}
- Lab meeting style: {xxx}

Academic Style Summary:
- Core hard rules: {xxx}
- Communication style: {xxx}
- Evaluation mode: {xxx}

Thinking Framework Summary:
- First instinct when facing a problem: {xxx}
- Methodological preferences: {xxx}
- Research trajectory: {xxx}

Confirm generation? Or need adjustments?
```

### Phase 5 — Write Files

Use `skill_writer.py` to create the directory structure and meta file, then write the content files:

```bash
# 1. Create directory structure
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action create-dir --slug {slug} --base-dir ./mentors

# 2. Write meta.json
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action write-meta \
  --slug {slug} --base-dir ./mentors \
  --name "{name}" --field "{field}" \
  --data-sources '["{source1}", "{source2}"]'
```

Then write the three content files using the Write tool (these require the generated content from Phase 4):

1. `mentors/{slug}/guidance.md`
2. `mentors/{slug}/style.md`
3. `mentors/{slug}/thinking_framework.md`

Finally, assemble the runnable SKILL.md from all components:

```bash
# 3. Assemble the final SKILL.md (combines guidance + style + thinking_framework)
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action assemble \
  --slug {slug} --base-dir ./mentors --name "{name}" --field "{field}"
```

The assembled `SKILL.md` automatically includes:
- All sub-commands (/{slug}, /{slug}-review, /{slug}-rewrite, /{slug}-advise)
- References to guidance.md, style.md, thinking_framework.md
- The anti-AI academic phrase blacklist
- Review, rewrite, and advise mode instructions

> Note: The full blacklist and mode instructions from `${CLAUDE_SKILL_DIR}/references/` and `${CLAUDE_SKILL_DIR}/prompts/` are referenced by path in the generated SKILL.md. If you need them fully inlined (e.g. for a standalone deployment), read and embed them manually.

Archive initial version:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action save --slug {slug} --base-dir ./mentors
```

### Phase 6 — Confirmation

```
✅ Mentor Skill created! Location: mentors/{slug}/

Available commands:
  /{slug}          — Daily conversation
  /{slug}-review   — Annotation-style paper review
  /{slug}-rewrite  — Demo rewrite
  /{slug}-advise   — Research direction advising

Something feel off? Just say "they wouldn't say that" and I'll correct it immediately.
```

---

## Workflow: Adding more data

When user provides additional materials for an existing mentor:

1. Process new data with the appropriate parser
2. Read `${CLAUDE_SKILL_DIR}/prompts/merger.md`
3. Determine which component(s) to update:
   - Contains guidance/feedback patterns → merge into guidance.md
   - Contains communication/personality signals → merge into style.md
   - Contains research/methodology patterns → merge into thinking_framework.md
   - Multiple aspects → merge into each respectively
4. Compare new vs existing content; append only incremental insights, never overwrite existing conclusions
5. Regenerate SKILL.md (merge latest guidance.md + style.md + thinking_framework.md)
6. Save new version via version_manager.py
7. Show user a change summary

---

## Workflow: Conversation correction

When user says things like "they wouldn't say that", "the tone is off", "they're much stricter than this", "they never praise people like that", or "ta不会这样说":

1. Read `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`
2. Identify whether the correction belongs to Guidance (scenarios/content) or Style (tone/behavior)
3. Write correction into the appropriate file's Correction layer
4. Takes effect immediately for all subsequent interactions
5. Correction layer max: 50 entries; when exceeded, consolidate and merge into main content

---

## Workflow: /list-mentors

Scan `./mentors/` directory. For each subdirectory with a valid `meta.json`, display:
- Slug, name, field, created_at, version, data_sources count

---

## Workflow: /mentor-rollback {slug} {version}

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./mentors
```

---

## Workflow: /delete-mentor {slug}

Confirm with user, then remove `mentors/{slug}/` directory entirely.
