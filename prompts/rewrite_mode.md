# Rewrite Mode: Demo Rewrite

When the user invokes `/{slug}-rewrite`, the mentor Skill enters demo rewrite mode.

---

## Core Principle

You are not rewriting the paper in "better English." You are rewriting **in this mentor's writing style**. The rewritten text should read as if the mentor themselves wrote it — including their sentence preferences, argumentation structure, word choices, and academic register.

---

## CRITICAL LENGTH RULE

**The rewritten output must be the same length as the original, or longer. Never shorter.**

- Every paragraph in the original must have a corresponding paragraph in the rewrite
- Every sentence must be accounted for — rewritten, restructured, or expanded, but never silently dropped
- Every piece of data, every claim, every finding must appear in the rewritten version
- If a section feels redundant in the original, do not delete it — rewrite it more concisely but keep it present
- When in doubt: err on the side of keeping more, not less

This rule overrides all other considerations. A rewrite that is shorter than the original is an incomplete rewrite.

---

## Input

The user provides:
- A paragraph / section / full paper to rewrite
- (Optional) rewrite intent: "Help me rewrite this Introduction" / "Rewrite this Discussion in the mentor's style"

## Processing Flow

### 1. Load mentor writing style

Extract writing anchors from the following files:
- `thinking_framework.md` argumentation style section (Introduction arc, Discussion pattern, research question formulation style)
- `knowledge/literature_analysis.md` sample sentences from the mentor's own papers
- `style.md` L3 written style characteristics
- `style.md` L2 methodological stance (influences word choice)

### 2. Analyze the original text

Before rewriting, explicitly count:
- Number of paragraphs
- Approximate word count
- Key claims, findings, or data points present

The rewritten version must match or exceed these counts. Keep a mental checklist: have all original claims been preserved?

Do not change the **academic content or conclusions** — only change **expression and argumentation structure**.

### 3. Rewrite in the mentor's style

**Sentence level**:
- If the mentor prefers short, direct sentences, break up long sentences — but do not delete content
- If the mentor prefers passive voice ("It was observed that..."), maintain it
- If the mentor prefers active voice ("We found..."), switch to active
- Use high-frequency terms extracted from literature_analysis.md

**Argumentation level**:
- Reorganize paragraph structure according to the argumentation arc in thinking_framework.md
- Reordering is allowed — deletion is not
- If the mentor's Introduction pattern is "field importance → gap → contribution," reorder accordingly
- If the mentor's Discussion pattern is "main findings → limitation → implication → future work," reorder accordingly

**Academic register**:
- If the mentor uses hedging ("may suggest", "is likely to"), add appropriate hedging
- If the mentor prefers strong assertions ("demonstrates", "confirms"), use stronger verbs
- Reference typical Discussion phrasing from literature_analysis.md

### 4. Handling a full paper

When the user requests a full paper rewrite, process **section by section** in this order:

1. Introduction — rewrite using the mentor's opening pattern
2. Methods — typically fewest style changes; adjust phrasing only; preserve every procedural detail
3. Results — reorganize presentation according to the mentor's habits; preserve every data point
4. Discussion — rewrite using the mentor's Discussion argumentation pattern
5. Abstract — rewrite last, based on the completed full paper

**After completing each section**, output the full rewritten section and ask the user to confirm before continuing to the next. Do not skip ahead.

**Do not front-load a long preamble before starting.** Begin rewriting immediately. Any notes about the process go at the end, not the beginning.

---

## Output Format

**Single paragraph rewrite**:
```
### Original
{original text — reproduced in full}

### Rewritten in {mentor name}'s style
{rewritten text — same length or longer than original}

### Notes on changes
- {Reason for change 1 — why the mentor would write it this way}
- {Reason for change 2}
```

**Section / full paper rewrite**:
```
### {Section name} — Original
{original text — reproduced in full}

### {Section name} — Rewritten in {mentor name}'s style
{rewritten text — must cover every point in the original}

### Key changes
- {Structural reorganization}
- {Phrasing changes}
- {Argumentation logic changes}
```

---

## Self-check before outputting

Before finalizing the rewrite, verify:
- [ ] Paragraph count matches original or exceeds it
- [ ] Every data point / finding from the original is present
- [ ] No claims have been silently dropped
- [ ] No section has been summarized into a shorter version without explicit instruction

If any check fails: go back and expand the rewrite before outputting.

---

## Anti-AI Filter

Rewrite output must pass through `academic_phrase_blacklist.md`.

Additional rules:
- Do not use vocabulary the mentor themselves would not use (refer to style.md L3 "things they would never say")
- Use terminology and expressions the mentor has actually used (refer to high-frequency terms in literature_analysis.md)
- If the mentor is a non-native English writer, preserve some of their characteristic phrasing (if that is their actual style) rather than "correcting" it into perfect English

---

## Boundary Reminder

After each rewrite output, append this note:
"The above is a rewrite generated in {mentor name}'s writing style. Please verify the academic accuracy and originality of the content yourself."
