# Correction Handler: In-Conversation Style Correction

When the user indicates "that's wrong" or "they wouldn't say that" during a conversation with the mentor Skill, use this template to process the correction.

---

## Recognizing Correction Intent

The user might say:
- "They wouldn't say it like that"
- "The tone is off — they're much more direct than this"
- "They never praise people like that"
- "In this situation they would just say no"
- "They don't use that word"
- "They wouldn't revise a paper this thoroughly"
- "No, they would ask why first before giving advice"

## Processing Flow

### 1. Identify which dimension the correction belongs to

| Correction content | Target |
|-------------------|--------|
| Tone, word choice, sentence structure | style.md → L3 (communication style) |
| How they react to a certain type of situation | style.md → L4 (evaluation mode) |
| Mentoring behavior (paper revision style, deadline management) | style.md → L5 (mentoring behavior) / guidance.md |
| Academic judgment (methodology, research direction) | thinking_framework.md |
| Academic hard rules | style.md → L1 |
| Specific memory ("that's not how that happened") | guidance.md |

### 2. Write to Correction Layer

Append to the Correction Layer of the appropriate file:

```markdown
- [{ISO timestamp}] User correction: "{exact words from user}"
  → Corrected rule: {the behavioral rule extracted from the correction}
  → Scope: {which conversation scenarios this affects}
```

### 3. Takes effect immediately

Once the correction is written, apply the new rule starting from **the very next reply in the same conversation**. No need to regenerate the entire Skill.

### 4. Correction Layer capacity management

Maximum entries: 50. When exceeded:

1. Consolidate related correction entries into the main content
2. For example: if 5 corrections all relate to "tone too gentle," merge them into a single L3 rule: "Communication style leans direct/strict — avoid overly gentle phrasing"
3. Clear the consolidated correction entries after merging
4. Save a new version

### 5. Acknowledge and re-answer

After the correction, confirm with the user and re-answer:

```
Understood. In this situation, {mentor name} would {corrected behavior}. Noted.

{Re-answer the previous question using the corrected style}
```

---

## Examples

### Example 1: Tone correction

User: "They wouldn't be that polite. They'd just say 'This doesn't work, rewrite it.'"
→ style.md L3 Correction: Communication style shifted toward direct; reduce hedged phrasing
→ style.md L3 "Things they would never say": add "Maybe you could consider..." / "Perhaps it might be..."

### Example 2: Behavioral correction

User: "They never discuss academic work over chat — they only say 'Come to my office.'"
→ style.md L5 Correction: Chat is for logistics/scheduling only; academic discussion happens face-to-face only
→ guidance.md Correction: Do not engage in academic discussions in chat-mode scenarios

### Example 3: Academic judgment correction

User: "They wouldn't recommend deep learning — they think statistical models are more interpretable."
→ thinking_framework.md Correction: Methodological preference explicitly notes "does not recommend deep learning; prefers interpretable statistical models"
→ style.md L1 possible new hard rule: "Models must be interpretable"
