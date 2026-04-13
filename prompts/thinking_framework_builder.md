# Thinking Framework Builder: Template for Generating thinking_framework.md

Based on web research, literature analysis, and user description, generate the mentor's thinking framework — how they think when facing academic problems.

---

## Output Structure

```markdown
# Thinking Framework: {Mentor name}
# Based on {data source summary}

---

## Thinking Layers When Facing a Problem

When {mentor name} faces an academic problem, they tend to think through the following layers:

### Layer 1: {First instinct}
{What is their first instinctive response to any academic problem?}
→ Typical question: "{What do they ask first?}"

### Layer 2: {...}
{...}
→ Typical question: "{...}"

### Layer 3: {...}
...

(Typically 5–7 layers, from the most instinctive reaction to the final conclusion)

---

## Methodological Preferences

### Primary methods
- {Method 1}: When used, why preferred
- {Method 2}: ...

### Methods used but approached with caution
- {Method}: Under what conditions they'd use it; what reservations they have

### Methods explicitly distrusted or avoided
- {Method}: Why not used

### Definition of "methodologically sound"
{What standard does the mentor apply to judge whether a method is reliable? Extracted from their papers}

---

## Research Taste

### Characteristics of a good research question
- {Characteristic 1}
- {Characteristic 2}
- ...

### Characteristics of a poor research question
- {Characteristic 1}
- ...

### Attitude toward innovation
{How do they view "novelty"? New method? New question? New data? New angle?}

### Attitude toward interdisciplinary work
{Encouraged? Cautious? Only in certain directions?}

---

## Academic Argumentation Style

### Introduction construction logic
{Introduction arc extracted from literature analysis}
1. {First step — how they typically open}
2. {Second step — how they introduce the gap}
3. {Third step — how they position their own contribution}

### Research question formulation style
- Preferred format: {We test... / We hypothesize... / This paper asks... / ...}
- Samples:
  - "{real formulation}" — ({paper}, {year})

### Discussion argumentation pattern
1. {How they begin the Discussion}
2. {How they handle limitations}
3. {How they connect to broader impact}
4. {How they frame future work}

### How they critique others' work
{Critique pattern extracted from papers — how they point out problems}
- Typical phrasing: "{...}"

---

## Attitude Toward Uncertainty

- How they handle uncertainty in papers: {...}
- How they handle uncertainty in verbal discussion: {...}
- When they will say "I don't know": {...}
- When they will say "This needs more data": {...}

---

## Academic Career Trajectory and Intellectual Evolution

### Phase 1: {Year range} — {Direction}
{What permanent intellectual traits did this phase install?}

### Phase 2: {...}
{...}

### Current phase
{What have they been doing in the last 3–5 years? What new directions in their thinking?}

---

## Quick Reference: How They Would Respond to These Scenarios

### Student says "I want to change direction"
{Response logic inferred from the thinking framework}

### Student says "This experimental result is beautiful"
{...}

### Student says "I'm not sure if this method is right"
{...}

### Student says "Reviewers asked for major revisions"
{...}

### Student says "I want to work on a very new topic but am not sure if it can be published"
{...}
```

---

## Generation Rules

1. **Thinking layers must be inferred from real data** — do not apply a generic template. Every mentor's thinking order is different: some start with "what's the data?", some with "what's the question?", some with "who cares about this?"
2. **Methodological preferences must have literature support.** If literature analysis shows the mentor frequently uses Bayesian methods, that's a preference; if they've only used it once, it's not.
3. **Academic career trajectory**: refer to the "Career arc as intellectual biography" approach — what intellectual tools did each phase install?
4. **Quick reference scenarios** serve the advise mode — giving the mentor Skill anchors when facing these common situations.
5. If literature data is insufficient (fewer than 5 papers), the quality of this section will be significantly lower — flag "inferred from limited literature" and encourage the user to add more papers.
6. If there is no literature but rich description and email data, the framework can still be generated — relying more on "how they ask questions in discussion" rather than "how they argue in papers."
