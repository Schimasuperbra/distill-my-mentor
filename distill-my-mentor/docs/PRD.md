# PRD: distill-my-mentor (Mentor Skill Creator)

## One-line description

Distill your academic mentor into an AI Skill that revises your papers, sets direction, and guides your research in their style.

## Background

Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill) and [dr-claw](https://github.com/OpenLAIR/dr-claw/). The mentor distiller applies the same framework to the academic mentoring relationship — your advisor graduated, retired, or moved on, but their academic style, mentoring approach, and thinking framework don't have to disappear.

## Core Features

### 1. Mentor Skill creation (/create-mentor)
- **Online research**: Input mentor name + institution; auto-searches Google Scholar, faculty pages, interviews, etc. to generate a baseline profile
- **Data collection**: Guided conversational intake for mentor style, supervision approach, catchphrases, etc.
- **Data import**: Supports WeChat/QQ/DingTalk/Feishu chat logs, email (.eml/.mbox/.msg), paper annotations (PDF annotations / Word track changes), literature folders (PDF directory), social media, photos
- **Three-track analysis**: Guidance (mentoring memory) + Style (academic style) + Thinking Framework
- **Generate Skill**: A standalone, runnable mentor Skill supporting four conversation modes

### 2. Four conversation modes
- **/{slug}**: Daily conversation — talk like you would with your mentor
- **/{slug}-review**: Annotation-style paper review — annotate section-by-section or full paper in the mentor's style
- **/{slug}-rewrite**: Demo rewrite — rewrite paragraphs or full papers in the mentor's writing style
- **/{slug}-advise**: Research direction advising — advice from the mentor's perspective + structured research outline

### 3. Continuous evolution
- **Add data**: Found more materials → auto-analyzes incremental content → merges into appropriate component
- **In-conversation correction**: Say "they wouldn't say that" → written to Correction layer → takes effect immediately
- **Version management**: Every change is auto-archived, with rollback support

## Three-Engine Architecture

| Engine | Content | File |
|--------|---------|------|
| Guidance | Mentoring memory: how they revise papers, run lab meetings, manage progress | guidance.md |
| Style | Academic style: five-layer structure (hard rules → identity → expression → evaluation → mentoring behavior) | style.md |
| Thinking Framework | Thinking framework: thinking layers for problems, methodological preferences, research taste | thinking_framework.md |

Runtime logic: message received → Style L1 hard rule check → Style L3 communication mode → Guidance retrieves relevant scenarios → Thinking Framework ensures academic consistency → anti-AI filter → output

## Data Sources

| Source | Parser tool | Origin |
|--------|------------|--------|
| WeChat chat logs | wechat_parser.py | ex-skill |
| QQ chat logs | qq_parser.py | ex-skill |
| Social media | social_parser.py | ex-skill |
| Photo EXIF | photo_analyzer.py | ex-skill |
| Mentor emails | email_parser.py | new |
| Paper annotations / reviewer responses | paper_comment_parser.py | new |
| Literature PDFs | literature_parser.py | new |

## Non-Goals

- Not a general academic writing assistant
- Not a plagiarism tool
- Not a replacement for the real mentoring relationship
- Not for impersonation in formal academic settings

## File Structure

```
distill-my-mentor/
├── SKILL.md                        # Main skill entry point
├── tools/                          # Data parsers and file managers
├── prompts/                        # Analysis and generation prompts
└── references/                     # Blacklists and discipline templates
    └── discipline_templates/
```
