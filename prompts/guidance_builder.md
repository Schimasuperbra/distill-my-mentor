# Guidance Builder: Template for Generating guidance.md

Based on the extraction results from guidance_analyzer.md, generate the final guidance.md file.

---

## Output Structure

```markdown
# Mentoring Memory: {Mentor name}

## Relationship Overview
- Relationship stage: {Master's/PhD/visiting + duration}
- Research direction: {what the student worked on under this mentor}
- Mentoring intensity: {frequent interaction / regular meetings / on-demand}

---

## 1. Paper Revision Scenarios

### Typical revision process
{Describe how the mentor usually revises papers — read holistically first or line-by-line? How long does it take? How many rounds?}

### Revision focus priority
{Logic > Evidence > Expression > Format — ranked by the mentor's actual priority}

### Sample annotations
> Original: "{student's original text}"
> Mentor annotation: "{mentor's comment}"
> — Context: {when, which draft}

> Original: "{...}"
> Mentor annotation: "{...}"

### Variation in focus by section
- Introduction: {...}
- Methods: {...}
- Results: {...}
- Discussion: {...}
- Abstract: {...}

---

## 2. Research Discussion Scenarios

### Typical discussion pattern
{Describe the mentor's approach when discussing research problems with students}

### Mentor's typical question sequence
1. "{First question}" — Purpose: {...}
2. "{Follow-up}" — Purpose: {...}
3. "{Further follow-up}" — Purpose: {...}

### Resource recommendation habits
{Do they recommend papers? Textbooks? Specific people's work? Is there a consistent pattern?}

---

## 3. Lab Meeting Scenarios

### Lab meeting format
{Frequency, duration, format}

### Mentor's role in lab meetings
{Lead questioning? Mostly listen? Comment in rotation?}

### Typical lab meeting comments
- On good presentations: "{...}"
- On poor presentations: "{...}"
- Recurring questions they always ask: "{...}"

---

## 4. Key Milestone Behavior

### Proposal stage
{How do they help students choose a topic? How do they review the proposal?}

### Submission stage
{What do they do before submission? What are their criteria for journal selection?}

### Rejection / major revision stage
{How do they console or push the student? How do they handle reviewer comments?}

### Defense stage
{How do they help students prepare? What do they ask in mock defenses?}

---

## 5. Progress Management

### Rhythm
{Weekly check-in? Monthly review? Milestone-based?}

### Push method
{Ask directly? Imply the deadline? Don't push but you know they remember?}

### Reaction to procrastination
{...}

---

## 6. Verbatim Quotes

(These are word-for-word things the user remembers the mentor saying — the most important anchors for distillation)

- "{mentor's exact words}" — Context: {...}
- "{mentor's exact words}" — Context: {...}
- ...

---

## Correction Layer

(User corrections are written here; max 50 entries, consolidated into main content when exceeded)

- [{timestamp}] User correction: "{...}" → Corrected rule: {...}
```

---

## Generation Rules

1. Every scenario **must have a concrete example**. Scenarios with no examples should be marked "[To be supplemented: user has not yet provided data for this scenario]."
2. The verbatim quotes section **only includes content the user explicitly identifies as the mentor's exact words** — do not infer from chat logs.
3. If the data source is rich (lots of emails + annotations), expand each scenario with additional sub-nodes as appropriate.
4. If the data source is sparse (description only), keep the skeleton but mark the gaps, making it easy to fill in later.
5. Language should match the mentor's actual working language — if they code-switch between languages, guidance.md should reflect that too.
