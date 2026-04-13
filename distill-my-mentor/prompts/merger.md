# Merger: Incremental Data Merge Logic

When the user provides new data for an existing mentor Skill, use this template to merge the incremental content.

---

## Trigger Conditions

User says: "I found some more emails", "Adding a few more chat logs", "Got another batch of papers", "Want to add some more description"

## Processing Flow

### 1. Analyze the type of new content

Determine which component the new content primarily updates:

| New content characteristics | Update target |
|----------------------------|--------------|
| Contains paper revision feedback, lab meeting discussion, research advising | → merge into `guidance.md` |
| Contains communication style, emotional pattern, relationship behavior signals | → merge into `style.md` |
| Contains papers / literature, methodology discussion, research direction | → merge into `thinking_framework.md` |
| Contains multiple types | → merge into each respective file |

### 2. Incremental vs. overwrite

**Principle: append incremental information only — never overwrite existing conclusions.**

Specific rules:
- New data **confirms** existing conclusions → add new evidence examples, increase confidence
- New data **enriches** existing conclusions → add new dimensions under existing entries
- New data **contradicts** existing conclusions → keep both, flag the contradiction, prompt user to confirm
- New data **fills a gap** → write directly into positions previously marked "to be supplemented"

### 3. Compare new vs. existing content

Before writing, generate a change summary:

```
Summary of new content:
- guidance.md: added {N} annotation examples, supplemented description of {scenario}
- style.md: L3 new catchphrase "{xxx}", L4 new reaction pattern for {scenario}
- thinking_framework.md: no change

Proceed with merge?
```

### 4. Execute merge

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action save --slug {slug} --base-dir ./mentors
```

Archive the current version first, then execute the merge, then regenerate SKILL.md (combining the latest guidance.md + style.md + thinking_framework.md).

### 5. Post-processing

- Check the merged files for duplicate content (same catchphrase appearing twice, etc.)
- Check whether the Correction Layer conflicts with new content (if the user previously corrected a behavior, does the new data reintroduce it?)
- If conflicts are found, prompt the user to confirm which version takes precedence

---

## Merge Examples

### Example: Adding email data

```
Existing guidance.md:
  Paper revision scenario → density: high → sample annotations: 2

New emails contain:
  3 emails with paper feedback; mentor replies inline, wording is stern

Merge operations:
  1. guidance.md → paper revision scenario → add 3 sample annotation examples
  2. style.md → L3 → add "email phrasing is more formal and stern than chat"
  3. thinking_framework.md → no change needed
```

### Example: Adding literature set

```
Existing thinking_framework.md:
  Methodological preference → primary method: regression analysis

New literature reveals:
  Mentor's papers in the last 3 years increasingly use machine learning methods

Merge operations:
  1. thinking_framework.md → methodological preference → add "emerging preference in recent years: machine learning methods"
  2. thinking_framework.md → academic timeline → add new phase
  3. knowledge/literature_analysis.md → update overall analysis
```
