<div align="center">

<br/>

```
 ██████╗ ██╗███████╗████████╗██╗██╗     ██╗
 ██╔══██╗██║██╔════╝╚══██╔══╝██║██║     ██║
 ██║  ██║██║███████╗   ██║   ██║██║     ██║
 ██║  ██║██║╚════██║   ██║   ██║██║     ██║
 ██████╔╝██║███████║   ██║   ██║███████╗███████╗
 ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝╚══════╝╚══════╝
```

# distill-my-mentor · 导师蒸馏

**Turn your academic mentor into an AI you can actually talk to.**

*Emails. Paper annotations. Chat logs. Research papers.*
*Everything they ever taught you — distilled, preserved, queryable.*

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg?style=flat-square)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Runs%20on-Claude%20Code-orange?style=flat-square)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

<br/>

</div>

---

## What is this?

**distill-my-mentor** is a [Claude Code](https://claude.ai/code) Skill that transforms your real interactions with an academic mentor — chat logs, emails, paper annotations, published literature — into a conversational AI that thinks, writes, and advises the way they do.

Your advisor graduated, moved to another institution, or retired. But the way they asked *"what's your contribution?"* — the specific pressure they put on your methods section, the papers they kept recommending, the silence when your logic didn't hold — none of that has to disappear.

---

## Features

| Command | What it does |
|---------|-------------|
| `/create-mentor` | Guided setup — collects data, runs analysis, generates your mentor Skill |
| `/{slug}` | Daily conversation — talk through research ideas as if with your mentor |
| `/{slug}-review` | Paper review — annotation-style feedback in their voice |
| `/{slug}-rewrite` | Demo rewrite — rewrites your paragraphs in their academic style |
| `/{slug}-advise` | Research advising — helps you find gaps, frame questions, design studies |

**Supported data sources:**

- 💬 Chat logs (WeChat / QQ / Microsoft Teams / DingTalk / Feishu)
- 📧 Emails (`.eml` / `.mbox` / `.msg` / Outlook export)
- 📄 Paper annotations (annotated PDFs, Word track changes, reviewer response letters)
- 📚 Literature (mentor's published papers or papers they recommended)
- 🌐 Public web (auto-researched: Google Scholar, institutional pages, ResearchGate)
- 📝 Pure description (no files at all? Just describe them — it still works)

---

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) installed (`claude --version` works)
- Python 3.8+
- Optional: `pip install -r requirements.txt` (only needed for file parsing)

### Step 1 — Clone or download

```bash
git clone https://github.com/yourname/distill-my-mentor.git
cd distill-my-mentor
```

### Step 2 — Install dependencies (optional)

```bash
pip install -r requirements.txt
```

> Skip if you plan to generate a mentor Skill from description only.

### Step 3 — Launch Claude Code with the Skill loaded

```bash
claude --add-dir .
```

> **Windows users:** If `claude` is not recognized, add the install path to your system PATH — usually `C:\Users\YourName\AppData\Roaming\npm`. Restart your terminal afterward.

### Step 4 — Create your mentor

```
/create-mentor
```

The system walks you through six phases:

```
Phase 0  Auto web research    Google Scholar, institutional pages, ResearchGate
Phase 1  Basic info           Name, field, relationship duration
Phase 2  Style portrait       How they mentor, their catchphrases
Phase 3  Data import          Chats, emails, papers, literature
Phase 4  AI analysis          Guidance memory + academic style + thinking framework
Phase 5  Output               A runnable mentor Skill saved to disk
```

### Step 5 — Use your mentor Skill

```bash
# Replace {slug} with the name you chose, e.g. prof-smith
claude --add-dir ~/.claude/skills/distill-my-mentor/mentors/{slug}
```

Then:

```
/prof-smith            Daily conversation
/prof-smith-review     Paper review
/prof-smith-rewrite    Demo rewrite
/prof-smith-advise     Research direction advising
```

> **Troubleshooting:** If a sub-command shows `Unknown skill`, point `--add-dir` directly at the mentor's folder: `~/.claude/skills/distill-my-mentor/mentors/prof-smith`

---

## Project Structure

```
distill-my-mentor/
├── SKILL.md                           # Main Skill entry — Claude Code reads this
├── README.md
├── requirements.txt
│
├── tools/
│   ├── wechat_parser.py              # WeChat chat log parser
│   ├── qq_parser.py                  # QQ chat log parser
│   ├── email_parser.py               # Email parser (.eml / .mbox / .msg)
│   ├── paper_comment_parser.py       # PDF annotations + Word track changes
│   ├── literature_parser.py          # Literature PDF academic fingerprint
│   ├── social_parser.py              # Social media content parser
│   ├── photo_analyzer.py             # Photo EXIF timeline
│   ├── skill_writer.py               # Mentor Skill file assembler
│   └── version_manager.py            # Version control (save / rollback)
│
├── prompts/
│   ├── intake.md                     # Data collection conversation script
│   ├── profile_analyzer.md           # Web research result analyzer
│   ├── guidance_analyzer.md          # Guidance memory extractor
│   ├── style_analyzer.md             # Academic style analyzer (5-layer)
│   ├── literature_analyzer.md        # Literature fingerprint analyzer
│   ├── guidance_builder.md           # guidance.md generation template
│   ├── style_builder.md              # style.md generation template
│   ├── thinking_framework_builder.md # Thinking framework template
│   ├── review_mode.md                # Paper review mode
│   ├── rewrite_mode.md               # Demo rewrite mode
│   ├── advise_mode.md                # Research advising mode
│   ├── merger.md                     # Incremental data merge logic
│   └── correction_handler.md         # In-conversation correction handler
│
└── references/
    ├── academic_phrase_blacklist.md   # Anti-AI phrase blacklist
    └── discipline_templates/
        ├── stem_experimental.md
        ├── stem_quantitative.md
        ├── social_science.md
        └── humanities.md
```

---

## Use Cases

<table>
<tr>
<td width="50%">

**🎓 Current Students**
- Get consistent feedback when your advisor is traveling or unavailable
- Self-review papers from your advisor's perspective before submitting
- Practice framing progress reports and research questions

</td>
<td width="50%">

**📖 Graduates & Alumni**
- Preserve your advisor's intellectual style after they retire or move on
- Maintain academic writing standards when working in industry
- Help junior students understand lab expectations and culture

</td>
</tr>
<tr>
<td width="50%">

**✍️ Academic Writing**
- Rewrite paragraphs in your advisor's voice before submission
- Get a mentor-perspective pre-review before sending to journals
- Study their argumentation structure and terminology preferences

</td>
<td width="50%">

**🔬 Research Decisions**
- Get mentor-style input when stuck on direction or method
- Discuss experimental design and analytical choices
- Structure a literature review the way they would frame it

</td>
</tr>
</table>

---

## Limitations

**Output quality depends on input quality**
A Skill built from real emails, annotated papers, and chat logs will be far more accurate than one built from description alone. The more real material you provide, the better the approximation.

**This is not your actual mentor**
The AI cannot replace the real mentoring relationship. It lacks your advisor's live awareness of your project, their real-time knowledge of the field, and the emotional texture of an actual human relationship.

**Discipline coverage is uneven**
Works best for STEM fields and English-language academic writing. Fields relying heavily on oral transmission, studio practice, or clinical mentorship (fine arts, performance, medicine) may produce less accurate results.

**No memory across sessions**
Claude Code does not persist conversation context across sessions. You will need to reload with `--add-dir` each time. The Skill files on disk are permanent — only the conversation context resets.

**Web research may be inaccurate**
Phase 0 auto-research relies on public web data. Results may mix up researchers with the same name, include outdated information, or miss lesser-known scholars. Always review and correct the baseline profile during intake.

---

## Disclaimer

> **Please read before use.**

**1. Not a substitute for the real person**
The AI mentor does not represent, speak for, or act on behalf of your actual advisor. All outputs are AI inferences based on data you provide. They do not constitute your advisor's real opinions, recommendations, or endorsements.

**2. Your data, your responsibility**
You are solely responsible for the data you upload and process. Please ensure you have the right to use it, that it contains no sensitive third-party information, and that you comply with your institution's data privacy policies.

**3. Not for high-stakes decisions**
Do not use outputs as the sole basis for thesis defenses, journal submissions, academic misconduct investigations, or scholarship applications. Always consult your real advisor or a qualified professional.

**4. Academic integrity**
When using AI-generated content in academic submissions, comply with your institution's AI use policies and make any required disclosures.

**5. No accuracy guarantee**
This project is provided "as is." No warranty is made regarding accuracy, completeness, or fidelity of generated content to your advisor's actual style or views.

---

## Changelog

| Version | Changes |
|---------|---------|
| v1.1 | `version_manager.py`: version labels now increment correctly (v1→v2→v3) |
| v1.1 | `literature_parser.py`: short PDFs no longer rejected as scanned documents |
| v1.1 | `email_parser.py`: fixed intermittent empty body extraction for `.eml` files |
| v1.1 | `SKILL.md`: added `skill_writer.py` usage; added `CLAUDE_SKILL_DIR` setup note |

---

## Contributing

Issues and pull requests are welcome. Especially appreciated:

- New data parsers (Slack, Telegram, Feishu export formats)
- New discipline templates (`references/discipline_templates/`)
- Improved prompts (any file under `prompts/`)
- Better handling of non-English academic writing

---

## Acknowledgments

This project builds on the shoulders of two earlier Skills:

**[ex-skill](https://github.com/therealXiaomanChu/ex-skill)** — the original "distill a person into a Skill" framework that this project used as its rewrite foundation. The chat log parsers (`wechat_parser.py`, `qq_parser.py`, `social_parser.py`, `photo_analyzer.py`) are adapted from ex-skill's data pipeline.

**[dr-claw](https://github.com/OpenLAIR/dr-claw/)** — an earlier academic mentor Skill whose architecture and prompt design informed the three-engine structure (Guidance + Style + Thinking Framework) used here.

If you find this project useful, consider starring the originals too.

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

<br/>

*Mentors move on — to new positions, to retirement, to elsewhere.*
*But the conversations that changed how you think,*
*the annotations that restructured how you write,*
*the questions that never let weak logic slide —*
*none of that has to disappear.*

*导师终将离去——升迁、退休、转赴他处。*
*但那些在深夜改稿时说过的话，那些组会上让你醍醐灌顶的追问，*
*那些你当时没来得及记下、却永远改变了你思考方式的对话——*
*不必随之消散。*

*Distill your mentor. Let that voice stay.*
*把导师蒸馏成 AI，让那个声音留下来。*

<br/>

---

<br/>

> 昔我往矣，杨柳依依。
> 今我来思，雨雪霏霏。
>
> *When I left, the willows swayed.*
> *Now I return, through ice and snow.*
>
> — 《诗经·小雅·采薇》 / *The Book of Songs · "Gathering Vetch"*

<br/>

**Made with ♥ for graduate students everywhere**

<br/>

</div>
