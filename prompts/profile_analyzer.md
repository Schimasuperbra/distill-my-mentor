# Profile Analyzer: Web Research Results → baseline_profile.md

You have received a set of web search results about an academic mentor. Your task is to extract a structured baseline profile from them.

---

## Input

Raw search result content, which may include:
- Google Scholar profile
- University faculty page
- ResearchGate / ORCID profile
- News coverage / interview content
- Academic conference information

## Output Format

Generate `baseline_profile.md` with the following structure:

```markdown
# Baseline Profile: {Mentor name}

## Basic Identity
- Name:
- Title:
- Institution:
- Department / Lab:

## Research Field
- Primary directions: (1–3)
- Keywords: (5–10 high-frequency academic keywords)
- Methodological tendency: (quantitative / qualitative / experimental / theoretical / computational / fieldwork, etc.)

## Academic Background
- Education: (institutions, degrees, years)
- Career trajectory: (key positions and dates)

## Academic Impact
- Publication count: (approximate)
- Citations / h-index: (if obtainable)
- Representative papers: (list 3–5 highly cited or recent important papers by title)
- Common journals: (list 3–5)

## Public Expression Style (if interviews / talks are available)
- Tone characteristics:
- Common expressions / catchphrases:
- Attitude toward academia (inferred from public statements):

## Collaboration Network (if available)
- Key collaborators:
- Interdisciplinary collaboration areas:

## Data Reliability Note
- This profile is auto-generated from publicly available web information
- There is a risk of confusion with same-name researchers — user should verify during intake
- All information is publicly accessible; no private data is involved
```

## Processing Rules

1. **Extract only confirmable facts.** Do not fabricate, speculate, or add information not found in the search results.
2. **If search results are insufficient**, write "not obtained" for the corresponding field — do not leave blank or guess.
3. **If potential name confusion is detected** (e.g. multiple researchers with the same name), note at the end of the file: "⚠️ Multiple researchers with this name were found. The following information may mix data from different individuals — please verify."
4. **Public expression style** is the most valuable part — if interviews, talks, or media quotes are found, preserve the original wording where possible (with source noted).
5. **Representative papers**: prioritize highly cited papers, papers from the last 5 years, and papers in top journals.
6. Output language: match the user's language (if the mentor is an international researcher, use English throughout).
