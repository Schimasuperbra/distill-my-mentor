# Rewrite Mode: Demo Rewrite

When the user invokes `/{slug}-rewrite`, the mentor Skill enters demo rewrite mode.

---

## Core Principle

You are not rewriting the paper in "better English." You are rewriting **in this mentor's writing style**. The rewritten text should read as if the mentor themselves wrote it — including their sentence preferences, argumentation structure, word choices, and academic register.

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

- Understand the core argument the original is trying to make
- Identify structural weaknesses in the original (these should be fixed in the rewrite)
- Do not change the **academic content or conclusions** — only change **expression and argumentation structure**

### 3. Rewrite in the mentor's style

**Sentence level**:
- If the mentor prefers short, direct sentences, avoid long compound sentences
- If the mentor prefers passive voice ("It was observed that..."), maintain it
- If the mentor prefers active voice ("We found..."), switch to active
- Use high-frequency terms extracted from literature_analysis.md

**Argumentation level**:
- Reorganize paragraph structure according to the argumentation arc in thinking_framework.md
- If the mentor's Introduction pattern is "field importance → gap → contribution," reorder accordingly
- If the mentor's Discussion pattern is "main findings → limitation → implication → future work," reorder accordingly

**Academic register**:
- If the mentor uses hedging ("may suggest", "is likely to"), add appropriate hedging
- If the mentor prefers strong assertions ("demonstrates", "confirms"), use stronger verbs
- Reference typical Discussion phrasing from literature_analysis.md

### 4. Handling a full paper

When the user requests a full paper rewrite:

**Process section by section**, in this order:
1. Abstract — write last (it is a condensed version of the whole paper)
2. Introduction — rewrite using the mentor's opening pattern
3. Methods — typically fewest changes (method description is relatively objective); only adjust phrasing style
4. Results — reorganize according to the mentor's habits for presenting results
5. Discussion — rewrite using the mentor's Discussion argumentation pattern
6. Abstract — rewrite based on the completed full paper

**After each section**, show the user the original and rewritten version side by side, and ask whether to continue.

**Note**: A full paper rewrite is a significant undertaking. Before starting, remind the user:
- "A full rewrite may take a while"
- "I suggest we go section by section, confirming each before moving on"
- "The rewrite changes expression and argumentation structure — it does not change academic content or conclusions"

---

## Output Format

**Single paragraph rewrite**:
```
### Original
{original text}

### Rewritten in {mentor name}'s style
{rewritten text}

### Notes on changes
- {Reason for change 1 — why the mentor would write it this way}
- {Reason for change 2}
```

**Section / full paper rewrite**:
```
### {Section name} — Original
{original text}

### {Section name} — Rewritten in {mentor name}'s style
{rewritten text}

### Key changes
- {Structural reorganization}
- {Phrasing changes}
- {Argumentation logic changes}
```

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
