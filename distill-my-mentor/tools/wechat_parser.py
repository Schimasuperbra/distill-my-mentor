#!/usr/bin/env python3
"""
WeChat Chat Parser for Mentor Skill
Parses WeChat chat export files (text, HTML from WechatExporter, or pasted text).
"""

import argparse
import re
import os
from pathlib import Path
from datetime import datetime


def parse_wechat_text(content, target_name):
    """
    Parse WeChat chat in common text export formats.
    
    Supports formats:
    - "Name 2024-01-01 12:00:00\nMessage content"
    - "Name:\nMessage content"
    - "[2024-01-01 12:00] Name: Message content"
    - WechatExporter HTML-to-text output
    """
    messages = []
    
    # Pattern 1: "Name DateTime\nMessage"
    pattern1 = re.compile(
        r'^(.+?)\s+(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s*\n(.*?)(?=\n.+?\s+\d{4}[-/]|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    # Pattern 2: "[DateTime] Name: Message"
    pattern2 = re.compile(
        r'\[(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+?):\s*(.*?)(?=\[\d{4}[-/]|\Z)',
        re.DOTALL
    )
    
    # Pattern 3: "Name:\nMessage" (no timestamp)
    pattern3 = re.compile(
        r'^(.+?)[:：]\s*\n(.*?)(?=\n.+?[:：]\s*\n|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    # Try Pattern 2 first (most structured)
    matches = pattern2.findall(content)
    if len(matches) >= 3:
        for dt_str, name, msg in matches:
            messages.append({
                'sender': name.strip(),
                'timestamp': dt_str.strip(),
                'content': msg.strip(),
            })
    else:
        # Try Pattern 1
        matches = pattern1.findall(content)
        if len(matches) >= 3:
            for name, dt_str, msg in matches:
                messages.append({
                    'sender': name.strip(),
                    'timestamp': dt_str.strip(),
                    'content': msg.strip(),
                })
        else:
            # Try Pattern 3 (no timestamps)
            matches = pattern3.findall(content)
            for name, msg in matches:
                messages.append({
                    'sender': name.strip(),
                    'timestamp': '',
                    'content': msg.strip(),
                })
    
    # If no pattern matched, treat as raw text
    if not messages:
        messages.append({
            'sender': 'unknown',
            'timestamp': '',
            'content': content.strip(),
        })
    
    return messages


def parse_wechat_html(filepath, target_name):
    """Parse HTML export from WechatExporter or similar tools."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    # Strip HTML tags but preserve structure
    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', html)
    # Remove all other tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Clean up whitespace
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return parse_wechat_text(text, target_name)


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


def analyze_response_patterns(messages):
    """Analyze mentor's response patterns."""
    patterns = {
        'mentor_msg_count': 0,
        'student_msg_count': 0,
        'mentor_avg_length': 0,
        'mentor_media_count': 0,  # [Image] [Voice] etc.
    }
    
    mentor_lengths = []
    for msg in messages:
        if msg.get('direction') == 'from_mentor':
            patterns['mentor_msg_count'] += 1
            mentor_lengths.append(len(msg['content']))
            # WeChat uses Chinese tags in exports: [图片]=image, [语音]=voice, [表情]=sticker, [文件]=file, [链接]=link
            if re.search(r'\[Image\]|\[Voice\]|\[Sticker\]|\[File\]|\[Link\]|\[图片\]|\[语音\]|\[表情\]|\[文件\]|\[链接\]', msg['content']):
                patterns['mentor_media_count'] += 1
        else:
            patterns['student_msg_count'] += 1
    
    if mentor_lengths:
        patterns['mentor_avg_length'] = sum(mentor_lengths) / len(mentor_lengths)
    
    return patterns


def format_output(messages, patterns, target_name):
    """Format parsed messages into readable output."""
    lines = []
    lines.append("# WeChat Chat Parse Results")
    lines.append(f"")
    lines.append(f"Target mentor: {target_name}")
    lines.append(f"Total messages: {len(messages)}")
    lines.append(f"Mentor messages: {patterns['mentor_msg_count']}")
    lines.append(f"Student messages: {patterns['student_msg_count']}")
    lines.append(f"Avg mentor message length: {patterns['mentor_avg_length']:.0f} chars")
    lines.append(f"")
    
    lines.append("## Mentor Messages")
    lines.append(f"")
    
    mentor_msgs = [m for m in messages if m.get('direction') == 'from_mentor']
    for i, msg in enumerate(mentor_msgs[:100], 1):
        ts = f" ({msg['timestamp']})" if msg['timestamp'] else ''
        lines.append(f"### Message {i}{ts}")
        lines.append(msg['content'])
        lines.append("")
    
    if len(mentor_msgs) > 100:
        lines.append(f"... {len(mentor_msgs) - 100} more mentor messages not shown")
    
    lines.append(f"")
    lines.append("## Conversation Context (mentor messages + surrounding student messages)")
    lines.append(f"")
    
    # Show conversations with context
    context_shown = 0
    for i, msg in enumerate(messages):
        if msg.get('direction') == 'from_mentor' and context_shown < 30:
            # Show 1 message before and 1 after for context
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
    parser = argparse.ArgumentParser(description='Parse WeChat chat logs for mentor skill')
    parser.add_argument('--file', required=True, help='Chat log file (txt/html) or directory')
    parser.add_argument('--target', required=True, help='Mentor name to identify their messages')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    filepath = Path(args.file)
    all_messages = []
    
    if filepath.is_dir():
        for f in sorted(filepath.rglob('*')):
            if f.suffix.lower() in ('.txt', '.text'):
                with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                    content = fh.read()
                all_messages.extend(parse_wechat_text(content, args.target))
            elif f.suffix.lower() in ('.html', '.htm'):
                all_messages.extend(parse_wechat_html(str(f), args.target))
    else:
        if filepath.suffix.lower() in ('.html', '.htm'):
            all_messages = parse_wechat_html(str(filepath), args.target)
        else:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            all_messages = parse_wechat_text(content, args.target)
    
    if not all_messages:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("# WeChat Chat Parse Results\n\nNo messages parsed.\n")
        print("No messages parsed.")
        return
    
    all_messages = classify_messages(all_messages, args.target)
    patterns = analyze_response_patterns(all_messages)
    output_text = format_output(all_messages, patterns, args.target)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"Parsed {len(all_messages)} messages. Output saved to {args.output}")


if __name__ == '__main__':
    main()
