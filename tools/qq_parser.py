#!/usr/bin/env python3
"""
QQ Chat Parser for Mentor Skill
Parses QQ chat export files (txt format from QQ message manager or copy-paste).
"""

import argparse
import re
from pathlib import Path


def parse_qq_text(content, target_name):
    """
    Parse QQ chat in common export formats.
    
    Supports formats:
    - QQ message manager export: "2024-01-01 12:00:00 Name(12345678)\nMessage content"
    - QQ copy-paste: "Name 12:00:00\nMessage content"
    - Merged forward: "Name: Message content"
    """
    messages = []
    
    # Pattern 1: QQ Manager export "DateTime Name(QQNumber)\nMessage"
    pattern1 = re.compile(
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}:\d{2})\s+(.+?)(?:\((\d+)\))?\s*\n(.*?)(?=\d{4}[-/]\d{1,2}[-/]|\Z)',
        re.DOTALL
    )
    
    # Pattern 2: "Name Time\nMessage"
    pattern2 = re.compile(
        r'^(.+?)\s+(\d{1,2}:\d{2}:\d{2})\s*\n(.*?)(?=\n.+?\s+\d{1,2}:\d{2}:\d{2}|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    # Try Pattern 1 first
    matches = pattern1.findall(content)
    if len(matches) >= 3:
        for dt_str, name, qq_num, msg in matches:
            messages.append({
                'sender': name.strip(),
                'timestamp': dt_str.strip(),
                'qq_number': qq_num.strip() if qq_num else '',
                'content': msg.strip(),
            })
    else:
        # Try Pattern 2
        matches = pattern2.findall(content)
        if len(matches) >= 3:
            for name, time_str, msg in matches:
                messages.append({
                    'sender': name.strip(),
                    'timestamp': time_str.strip(),
                    'qq_number': '',
                    'content': msg.strip(),
                })
    
    if not messages:
        messages.append({
            'sender': 'unknown',
            'timestamp': '',
            'qq_number': '',
            'content': content.strip(),
        })
    
    return messages


def classify_messages(messages, target_name):
    """Classify messages as from_mentor or from_student."""
    target_lower = target_name.lower() if target_name else ''
    
    for msg in messages:
        sender = msg['sender'].lower()
        if target_lower and (target_lower in sender or sender in target_lower):
            msg['direction'] = 'from_mentor'
        else:
            msg['direction'] = 'from_student'
    
    return messages


def format_output(messages, target_name):
    """Format results into readable output."""
    lines = []
    lines.append("# QQ Chat Parse Results")
    lines.append("")
    lines.append(f"Target mentor: {target_name}")
    lines.append(f"Total messages: {len(messages)}")
    
    mentor_msgs = [m for m in messages if m.get('direction') == 'from_mentor']
    student_msgs = [m for m in messages if m.get('direction') == 'from_student']
    lines.append(f"Mentor messages: {len(mentor_msgs)}")
    lines.append(f"Student messages: {len(student_msgs)}")
    lines.append("")
    
    lines.append("## Mentor Messages")
    lines.append("")
    for i, msg in enumerate(mentor_msgs[:100], 1):
        ts = f" ({msg['timestamp']})" if msg['timestamp'] else ''
        lines.append(f"### Message {i}{ts}")
        lines.append(msg['content'][:500])
        lines.append("")
    
    lines.append("## Conversation Excerpts (with context)")
    lines.append("")
    context_shown = 0
    for i, msg in enumerate(messages):
        if msg.get('direction') == 'from_mentor' and context_shown < 30:
            start = max(0, i - 1)
            end = min(len(messages), i + 2)
            lines.append(f"### Excerpt {context_shown + 1}")
            for j in range(start, end):
                m = messages[j]
                role = "Mentor" if m.get('direction') == 'from_mentor' else "Student"
                ts = f" {m['timestamp']}" if m['timestamp'] else ''
                lines.append(f"[{role}]{ts}: {m['content'][:300]}")
            lines.append("")
            context_shown += 1
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse QQ chat logs for mentor skill')
    parser.add_argument('--file', required=True, help='Chat log file (txt)')
    parser.add_argument('--target', required=True, help='Mentor name')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()
    
    filepath = Path(args.file)
    
    if filepath.is_dir():
        content = ""
        for f in sorted(filepath.rglob('*.txt')):
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                content += fh.read() + "\n"
    else:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    
    messages = parse_qq_text(content, args.target)
    messages = classify_messages(messages, args.target)
    output_text = format_output(messages, args.target)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"Parsed {len(messages)} messages. Output saved to {args.output}")


if __name__ == '__main__':
    main()
