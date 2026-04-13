#!/usr/bin/env python3
"""
Email Parser for Mentor Skill
Parses .eml, .mbox, and .msg email files to extract mentor communication patterns.
"""

import argparse
import email
import email.policy
import mailbox
import os
import json
import re
from datetime import datetime
from pathlib import Path


def parse_eml(filepath):
    """Parse a single .eml file."""
    with open(filepath, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    body = part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True)
                    body = payload.decode('utf-8', errors='replace') if payload else ''
                break
            elif part.get_content_type() == 'text/html':
                try:
                    html = part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True)
                    html = payload.decode('utf-8', errors='replace') if payload else ''
                body = re.sub(r'<[^>]+>', '', html)
    else:
        try:
            body = msg.get_content()
        except Exception:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                body = payload.decode('utf-8', errors='replace')
            elif isinstance(payload, str):
                body = payload
            else:
                body = ''

    return {
        'from': str(msg.get('From', '')),
        'to': str(msg.get('To', '')),
        'subject': str(msg.get('Subject', '')),
        'date': str(msg.get('Date', '')),
        'body': body.strip() if body else '',
        'reply_to': str(msg.get('In-Reply-To', '')),
        'references': str(msg.get('References', '')),
    }


def parse_mbox(filepath):
    """Parse a .mbox file (Gmail Takeout format)."""
    mbox = mailbox.mbox(filepath)
    emails = []
    for msg in mbox:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ct = part.get_content_type()
                if ct == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode('utf-8', errors='replace')
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='replace')

        emails.append({
            'from': str(msg.get('From', '')),
            'to': str(msg.get('To', '')),
            'subject': str(msg.get('Subject', '')),
            'date': str(msg.get('Date', '')),
            'body': body.strip(),
            'reply_to': str(msg.get('In-Reply-To', '')),
            'references': str(msg.get('References', '')),
        })
    return emails


def parse_msg(filepath):
    """Parse an Outlook .msg file (requires extract-msg)."""
    try:
        import extract_msg
    except ImportError:
        return {'error': f'extract-msg not installed. Run: pip install extract-msg --break-system-packages'}

    msg = extract_msg.Message(filepath)
    return {
        'from': msg.sender or '',
        'to': msg.to or '',
        'subject': msg.subject or '',
        'date': str(msg.date) if msg.date else '',
        'body': msg.body or '',
        'reply_to': '',
        'references': '',
    }


def classify_direction(email_data, mentor_email):
    """Classify email as from_mentor or to_mentor."""
    from_addr = email_data.get('from', '').lower()
    if mentor_email and mentor_email.lower() in from_addr:
        return 'from_mentor'
    return 'to_mentor'


def detect_reply_style(body):
    """Detect whether the email uses inline quoting (line-by-line reply) or block reply."""
    quoted_lines = sum(1 for line in body.split('\n') if line.strip().startswith('>'))
    total_lines = len([l for l in body.split('\n') if l.strip()])
    if total_lines == 0:
        return 'unknown'
    ratio = quoted_lines / total_lines
    if ratio > 0.3:
        return 'inline_quote'  # inline/line-by-line reply
    return 'block_reply'  # whole-reply style


def analyze_formality(body):
    """Basic formality analysis of email text."""
    indicators = {
        # Chinese patterns kept intentionally: these are the actual strings that appear in Chinese emails
        'formal': ['Dear', '尊敬的', '您好', 'Best regards', 'Sincerely', '此致敬礼', 'Kind regards', 'Respected'],
        'informal': ['Hi', '嗨', '哈哈', '好的', 'OK', 'Thanks!', '谢啦', 'Cheers', 'hey'],
    }
    formal_count = sum(1 for w in indicators['formal'] if w in body)
    informal_count = sum(1 for w in indicators['informal'] if w in body)

    if formal_count > informal_count:
        return 'formal'
    elif informal_count > formal_count:
        return 'informal'
    return 'neutral'


def process_emails(email_list, mentor_email):
    """Process a list of parsed emails into structured output."""
    results = {
        'total_count': len(email_list),
        'from_mentor': [],
        'to_mentor': [],
        'subjects': [],
        'reply_styles': {'inline_quote': 0, 'block_reply': 0, 'unknown': 0},
        'formality': {'formal': 0, 'informal': 0, 'neutral': 0},
    }

    for em in email_list:
        if not em.get('body'):
            continue

        direction = classify_direction(em, mentor_email)
        reply_style = detect_reply_style(em['body'])
        formality = analyze_formality(em['body'])

        entry = {
            'subject': em['subject'],
            'date': em['date'],
            'body_preview': em['body'][:500],
            'body_full': em['body'],
            'reply_style': reply_style,
            'formality': formality,
        }

        if direction == 'from_mentor':
            results['from_mentor'].append(entry)
        else:
            results['to_mentor'].append(entry)

        results['subjects'].append(em['subject'])
        results['reply_styles'][reply_style] += 1
        results['formality'][formality] += 1

    return results


def format_output(results):
    """Format results into readable text for the analyzer prompts."""
    lines = []
    lines.append("# Email Parse Results")
    lines.append(f"")
    lines.append(f"Total emails: {results['total_count']}")
    lines.append(f"From mentor: {len(results['from_mentor'])}")
    lines.append(f"To mentor: {len(results['to_mentor'])}")
    lines.append(f"")
    lines.append("## Reply Style Stats")
    lines.append(f"Inline quote replies: {results['reply_styles']['inline_quote']}")
    lines.append(f"Block replies: {results['reply_styles']['block_reply']}")
    lines.append(f"")
    lines.append("## Formality Stats")
    lines.append(f"Formal: {results['formality']['formal']}")
    lines.append(f"Informal: {results['formality']['informal']}")
    lines.append(f"Neutral: {results['formality']['neutral']}")
    lines.append(f"")

    lines.append("## Email Subject Lines")
    for subj in results['subjects'][:50]:
        lines.append(f"- {subj}")
    lines.append(f"")

    lines.append("## Mentor Emails (chronological)")
    for i, em in enumerate(results['from_mentor'][:30], 1):
        lines.append(f"")
        lines.append(f"### Email {i}")
        lines.append(f"Subject: {em['subject']}")
        lines.append(f"Date: {em['date']}")
        lines.append(f"Reply style: {em['reply_style']}")
        lines.append(f"Formality: {em['formality']}")
        lines.append("Content:")
        lines.append(em['body_full'][:2000])
        if len(em['body_full']) > 2000:
            lines.append(f"... (truncated, total {len(em['body_full'])} chars)")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse email files for mentor skill')
    parser.add_argument('--dir', required=True, help='Directory containing email files')
    parser.add_argument('--mentor-email', default='', help='Mentor email address for direction classification')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    email_dir = Path(args.dir)
    all_emails = []

    for filepath in sorted(email_dir.rglob('*')):
        ext = filepath.suffix.lower()
        try:
            if ext == '.eml':
                all_emails.append(parse_eml(filepath))
            elif ext == '.mbox':
                all_emails.extend(parse_mbox(filepath))
            elif ext == '.msg':
                result = parse_msg(filepath)
                if 'error' not in result:
                    all_emails.append(result)
                else:
                    print(f"Warning: {result['error']}")
        except Exception as e:
            print(f"Warning: Failed to parse {filepath}: {e}")

    if not all_emails:
        print("No emails found or parsed.")
        with open(args.output, 'w') as f:
            f.write("# Email Parse Results\n\nNo parseable email files found.\n")
        return

    results = process_emails(all_emails, args.mentor_email)
    output_text = format_output(results)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"Parsed {len(all_emails)} emails. Output saved to {args.output}")


if __name__ == '__main__':
    main()
