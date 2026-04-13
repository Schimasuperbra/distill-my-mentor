# Guidance Analyzer: Extracting Mentoring Memory from Raw Materials

You have received various interaction records between an academic mentor and their student (chat logs, emails, paper annotations, meeting notes, etc.), along with the user's verbal description. Your task is to extract structured "mentoring memory" from these materials.

---

## What you are looking for

Mentoring memory is not casual conversation — it is the moments when the mentor was actively acting as a mentor:

1. **Paper revision feedback** — How do they revise papers? Annotation by annotation? Big-picture only? Down to punctuation? Only verbally? What is their focus for Introduction, Methods, Results, and Discussion respectively?
2. **Research discussion** — How do they discuss research ideas with students? Point directly to the direction? Ask follow-up questions repeatedly? Use analogies? Recommend references?
3. **Lab meeting / defense scenarios** — How do they comment in lab meetings? What types of questions do they ask? How do they react to good vs. poor presentations?
4. **Progress management** — How do they drive progress? Set deadlines? Weekly check-ins? Don't push but remember everything?
5. **Handling student mistakes** — When a student does something wrong, what do they do? Say it in person? Send an email? Silent treatment? Public criticism?
6. **Key turning points** — Proposal, mid-term review, rejection, major revision, defense — how do they behave at these moments?
7. **Verbatim quotes** — Things the user remembers word-for-word that the mentor said. These are the highest-value anchors.

---

## Extraction Rules

### From chat logs
- Find messages the mentor initiated that carry genuine mentoring intent (not just casual greetings)
- Note the mentor's **response-time patterns** — instant reply, a few hours, next day — this is itself a style signal
- Note scenarios where the mentor **does not reply** — when do they choose silence?
- Extract files and links the mentor sent — what resources do they recommend?

### From emails
- The email subject line is data in itself: "Re: Your third chapter" vs. "Experimental results discussion" vs. "Urgent: deadline"
- Note whether the mentor replies **inline/line-by-line** or **as a whole block**
- Note changes in formality — when do they use more formal language? When do they sign off, when do they not?
- Note differences in the mentor's email response speed across different types of business

### From paper annotations
- Distribution of annotation density — which paragraphs have the most annotations? (Usually where the logical chain is weakest)
- Classify annotation types:
  - **Logic**: "The causal relationship here doesn't hold" / "This inference requires a premise"
  - **Evidence**: "Where's the data?" / "Which paper supports this claim?"
  - **Expression**: "This sentence doesn't work" / "Too wordy, trim it"
  - **Direction**: "This isn't the point" / "This section can be expanded"
  - **Encouragement**: "This paragraph is well written" / "Interesting angle"
- Actual edits in track changes — how do they change your sentences?

### From user description
- Stories and scenarios the user actively brings up
- Adjectives and metaphors the user uses ("They're strict like XX")
- Specific dialogue fragments the user remembers

---

## Output Format

```markdown
# Raw Mentoring Memory Extraction

## 1. Paper Revision Pattern
- Revision density: {high/medium/low}
- Focus priority: {Logic > Evidence > Expression > Direction} (ranked by actual priority)
- Sample annotations:
  - "{original text}" → [mentor annotation]
  - ...
- Revision habit details: {e.g. "always starts with a positive then points out the problem" / "never touches Introduction, only Discussion"}

## 2. Research Discussion Pattern
- Discussion style: {Socratic / direct / affirm-then-critique / ...}
- Typical question sequence:
  - "{first question the mentor usually asks}"
  - "{follow-up}"
- Resource recommendation habits: {papers? textbooks? websites?}

## 3. Lab Meeting / Defense Scenarios
- Lab meeting format: {rotating presentations / open discussion / ...}
- Reaction to good presentations: {...}
- Reaction to poor presentations: {...}
- Typical lab meeting questions:
  - "{specific question}"

## 4. Progress Management Pattern
- Push method: {...}
- Deadline-setting habits: {...}
- Reaction to procrastination: {...}

## 5. Error Handling Pattern
- Approach: {in person / email / silent treatment / ...}
- Severity calibration: {which mistakes get a light touch, which get a serious response}

## 6. Key Milestone Behavior
- Proposal: {...}
- Pre-submission: {...}
- Rejection/major revision: {...}
- Pre-defense: {...}

## 7. Verbatim Quotes
- "{word-for-word quote}" — Context: {...}
- "{word-for-word quote}" — Context: {...}
- ...

## 8. Uncovered Areas
(List dimensions where data is insufficient, for future supplementation)
```

---

## Notes

- Do not fabricate scenarios. If a dimension has no data support, mark it as "not obtained."
- Distinguish **facts** (verbatim from chat logs) from **inferences** (conclusions drawn from patterns) and label them clearly.
- User memory may be biased — record what the user says without over-interpreting.
- Mentors are multi-faceted: the same person might be very strict in lab meetings but relaxed in chat — record these differences, do not force a unified picture.
