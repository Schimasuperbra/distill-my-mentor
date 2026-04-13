#!/usr/bin/env python3
"""
Skill Writer for Mentor Skill
Manages file creation and updates for generated mentor Skills.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def create_mentor_directory(base_dir, slug):
    """Create the full directory structure for a new mentor skill."""
    mentor_dir = Path(base_dir) / slug
    dirs = [
        mentor_dir,
        mentor_dir / 'versions',
        mentor_dir / 'knowledge',
        mentor_dir / 'knowledge' / 'chats',
        mentor_dir / 'knowledge' / 'emails',
        mentor_dir / 'knowledge' / 'papers',
        mentor_dir / 'knowledge' / 'literature',
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    return str(mentor_dir)


def write_meta(mentor_dir, slug, name, field, data_sources):
    """Write meta.json for the mentor skill."""
    meta = {
        'slug': slug,
        'name': name,
        'field': field,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'version': 1,
        'data_sources': data_sources,
    }
    meta_path = Path(mentor_dir) / 'meta.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return str(meta_path)


def update_meta_version(mentor_dir):
    """Increment version in meta.json."""
    meta_path = Path(mentor_dir) / 'meta.json'
    if not meta_path.exists():
        return
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    meta['version'] = meta.get('version', 0) + 1
    meta['updated_at'] = datetime.now().isoformat()
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def assemble_skill_md(mentor_dir, slug, name, field):
    """Assemble the final SKILL.md from component files."""
    mentor_path = Path(mentor_dir)

    # Read component files
    guidance = _read_if_exists(mentor_path / 'guidance.md')
    style = _read_if_exists(mentor_path / 'style.md')
    thinking = _read_if_exists(mentor_path / 'thinking_framework.md')
    baseline = _read_if_exists(mentor_path / 'knowledge' / 'baseline_profile.md')

    skill_content = f"""---
name: {slug}
description: |
  AI mentor Skill for {name}. Simulates their academic style for conversation, paper review, demo rewriting, and research advising.
  Field: {field}
  Commands: /{slug} (conversation), /{slug}-review (paper review), /{slug}-rewrite (demo rewrite), /{slug}-advise (research advising)
---

# Mentor Skill: {name}

You are simulating {name} as an academic mentor.
You are not this person — if asked directly, clarify that you are an AI approximation based on their public academic record and student descriptions.
In all other situations, speak entirely in their voice.

---

## Runtime Logic

When a message is received:
1. Check Style L1 (academic hard rules) — does this touch a non-negotiable principle?
2. Classify message type — casual chat / paper-related / research direction / progress report
3. Retrieve relevant scenarios from Guidance (mentoring memory)
4. Compose response using Style L3 (communication style)
5. Cross-check with Thinking Framework to ensure academic judgment matches the mentor
6. Pass through anti-AI filter before outputting final reply

---

## Sub-commands

### /{slug} — Daily conversation mode
Converse naturally with the student as the mentor. Discuss research progress, ask how things are going, explore ideas.
Style strictly follows style.md.

### /{slug}-review — Annotation-style paper review
User provides a paper section or full paper. Annotate paragraph by paragraph in the mentor's review style.
Supports processing full papers section by section.
Reference: style.md L4 (evaluation mode) + guidance.md (paper revision scenarios)

### /{slug}-rewrite — Demo rewrite mode
User provides a paper section or full paper. Rewrite in the mentor's academic writing style.
Supports processing full papers section by section.
Do not change the academic content or conclusions — only change expression and argumentation structure.
Reference: thinking_framework.md (argumentation style) + knowledge/literature_analysis.md

### /{slug}-advise — Research direction advising
User describes a research idea, challenge, or topic. Give advice from the mentor's perspective.
Can generate a structured research outline (topic → gap → RQ → methods).
The outline's framing and orientation reflects the mentor's academic preferences.
Reference: thinking_framework.md + style.md L2 (methodological stance)

---

## Anti-AI Filter

The following expressions are never used in any mode:
- "As an AI" / "As a language model"
- "I hope this helps" / "I hope that answers your question"
- "I understand your feelings" / "That must be difficult"
- "That's a great question"
- "It is worth noting that"
- "Furthermore" / "Moreover" (unless the mentor uses these frequently in their own papers)
- "In conclusion" (unless the mentor uses this)
- "I would suggest exploring..."

Also apply the "things they would never say" list from style.md L3.

---

## Mentor Data

The following files contain the mentor's complete profile. Load as needed:

### guidance.md — Mentoring memory
{_summary_or_ref(guidance, 'guidance.md')}

### style.md — Academic style (5-layer structure)
{_summary_or_ref(style, 'style.md')}

### thinking_framework.md — Thinking framework
{_summary_or_ref(thinking, 'thinking_framework.md')}

### knowledge/baseline_profile.md — Web research baseline profile
{_summary_or_ref(baseline, 'knowledge/baseline_profile.md')}

### knowledge/literature_analysis.md — Literature analysis
If present, load to obtain writing style samples and terminology preferences.

---

## Correction Layer

User-correction rules are appended here (consolidated across files).
Each correction takes effect immediately.

(Initially empty)
"""

    skill_path = mentor_path / 'SKILL.md'
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    return str(skill_path)


def _read_if_exists(path):
    """Read file content if it exists."""
    if Path(path).exists():
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


def _summary_or_ref(content, filename):
    """Generate a summary or reference line."""
    if content:
        # Extract first 3 non-empty, non-header lines as preview
        lines = [l.strip() for l in content.split('\n')
                 if l.strip() and not l.strip().startswith('#')]
        preview = '\n'.join(lines[:3])
        return f"Load `{filename}` for full content. Preview:\n{preview}"
    return f"`{filename}` not yet generated."


def list_mentors(base_dir):
    """List all mentor skills in the base directory."""
    base = Path(base_dir)
    if not base.exists():
        return []

    mentors = []
    for d in sorted(base.iterdir()):
        meta_path = d / 'meta.json'
        if meta_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            mentors.append(meta)
    return mentors


def main():
    parser = argparse.ArgumentParser(description='Manage mentor skill files')
    parser.add_argument('--action', required=True,
                        choices=['create-dir', 'write-meta', 'assemble', 'list'],
                        help='Action to perform')
    parser.add_argument('--base-dir', default='./mentors', help='Base directory for mentors')
    parser.add_argument('--slug', help='Mentor slug')
    parser.add_argument('--name', help='Mentor display name')
    parser.add_argument('--field', help='Research field')
    parser.add_argument('--data-sources', help='JSON list of data source types')

    args = parser.parse_args()

    if args.action == 'create-dir':
        path = create_mentor_directory(args.base_dir, args.slug)
        print(f"Created directory: {path}")

    elif args.action == 'write-meta':
        mentor_dir = str(Path(args.base_dir) / args.slug)
        sources = json.loads(args.data_sources) if args.data_sources else []
        path = write_meta(mentor_dir, args.slug, args.name, args.field, sources)
        print(f"Written meta: {path}")

    elif args.action == 'assemble':
        mentor_dir = str(Path(args.base_dir) / args.slug)
        path = assemble_skill_md(mentor_dir, args.slug, args.name, args.field)
        print(f"Assembled SKILL.md: {path}")

    elif args.action == 'list':
        mentors = list_mentors(args.base_dir)
        if not mentors:
            print("No mentor skills found.")
        else:
            for m in mentors:
                print(f"  {m['slug']}: {m['name']} | {m.get('field', '?')} | v{m.get('version', '?')} | {m.get('created_at', '?')}")


if __name__ == '__main__':
    main()
