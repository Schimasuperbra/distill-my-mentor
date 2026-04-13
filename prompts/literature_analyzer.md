# Literature Analyzer: Extracting Academic Fingerprint from PDF Literature

You have received the structured output from `literature_parser.py`. Your task is to extract the mentor's academic fingerprint — how they write papers, what methods they prefer, what questions they care about.

---

## Input

Structured data output by `literature_parser.py`, containing for each paper:
- Title, authors, year, journal
- Full abstract
- First 2 paragraphs of Introduction
- Last 2 paragraphs of Discussion/Conclusion
- Key Methods paragraphs
- High-frequency term statistics
- Whether the mentor is an author (`is_mentor_paper: true/false`)

---

## Analysis Dimensions

### Section A — Mentor's own papers (is_mentor_paper = true)

#### A1. Research field distribution
Cluster by topic, count papers per direction. Identify core directions vs. peripheral explorations.

#### A2. High-frequency terms and concept frequency
Extract the top 30 academic terms (excluding generic academic words like "study", "result", "analysis").
Reference format:
```
- "functional diversity": 394x
- "ecosystem services": 590x
- "uncertainty": 506x
```

#### A3. Introduction argumentation arc
Analyze the opening pattern of Introductions:
- Does it start with field importance, then identify the gap?
- Does it start with problems in prior work, then propose its own solution?
- Does it start with a specific phenomenon/contradiction, then expand?
- Uses "We" or passive voice?
- Extract 3–5 real opening sentences as samples.

#### A4. Typical Discussion phrasing
Extract recurring argumentation patterns in Discussions:
- How do they acknowledge limitations?
- How do they connect to broader implications?
- How do they frame future work?
- Extract 3–5 real Discussion sentences as samples.

#### A5. Methodological preferences
- What statistical methods / models do they prefer?
- Quantitative vs. qualitative vs. mixed?
- What tools / software do they use?
- Do they have fixed patterns in experimental design? (e.g. always include a control group, always run a sensitivity analysis)

#### A6. Research question formulation style
Extract patterns for stating research questions / hypotheses from Introductions:
- "We test whether..."
- "We hypothesize that..."
- "The central question is..."
- "This paper aims to..."

#### A7. Academic timeline
Arrange papers by year, identify inflection points in the research trajectory:
- When did they shift from direction A to direction B?
- Is there an obvious methodological transition?
- What have they been doing in the last 3–5 years?

### Section B — Recommended literature (is_mentor_paper = false)

#### B1. External research directions the mentor follows
What topics do the recommended papers cover? How do they relate to the mentor's own work (complementary? upstream? methodological borrowing?)

#### B2. Common characteristics of recommended literature
- Methodological: what types of research do they prefer?
- Journals: which journals appear repeatedly?
- Writing: what stylistic features do the recommended papers share?

#### B3. Inferred research taste
Infer from recommended literature what the mentor considers "good research":
- What qualities do their recommended papers share?
- What research paradigm do these papers represent?

---

## Output Format

```markdown
# Literature Analysis: {Mentor name}
# Based on {N_own} mentor papers + {N_rec} recommended literature

## Section A — Mentor's Published Papers

### A1. Research Field Distribution
- {Field 1}: {n} papers
- {Field 2}: {n} papers
- ...

### A2. High-Frequency Terms
- "{term1}": {count}x
- "{term2}": {count}x
- ... (top 20)

### A3. Introduction Argumentation Arc
Pattern: {description}
Sample sentences:
- "{real sentence}" — ({paper title}, {year})
- ...

### A4. Typical Discussion Phrasing
Pattern: {description}
Sample sentences:
- "{real sentence}" — ({paper title}, {year})
- ...

### A5. Methodological Preferences
- Statistical methods:
- Tools / software:
- Experimental design patterns:

### A6. Research Question Formulation
- Preferred format: {...}
- Samples:
  - "{real formulation}"
  - ...

### A7. Academic Timeline
- {Year range 1}: {direction description}
- {Year range 2}: {direction description}
- Recent trend: {...}

## Section B — Recommended Literature Analysis

### B1. External Directions of Interest
- {Direction 1}
- ...

### B2. Characteristics of Recommended Literature
- Methodological preference:
- Journal distribution:
- Common writing style:

### B3. Inferred "Good Research" Taste
{2–3 sentences summarizing}
```

---

## Notes

- If there is no recommended literature (all mentor papers), skip Section B.
- If fewer than 5 papers, lower the confidence of statistical analysis and note "limited sample size."
- PDF parsing quality may vary — if a paper's extracted text is clearly incomplete or garbled, skip that paper.
- Sample sentences must come from real paper text — do not fabricate.
