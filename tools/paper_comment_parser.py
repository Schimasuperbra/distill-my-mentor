#!/usr/bin/env python3
"""
Paper Comment Parser for Mentor Skill
Extracts annotations from PDFs and track changes from Word documents.
"""

import argparse
import json
import os
import re
from pathlib import Path


def parse_pdf_annotations(filepath):
    """Extract annotations/comments/highlights from a PDF file."""
    try:
        import fitz  # pymupdf
    except ImportError:
        return {'error': 'pymupdf not installed. Run: pip install pymupdf --break-system-packages'}

    doc = fitz.open(filepath)
    annotations = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        for annot in page.annots() or []:
            annot_type = annot.type[1]  # e.g., 'Text', 'Highlight', 'StrikeOut', 'FreeText'
            content = annot.info.get('content', '') or ''
            subject = annot.info.get('subject', '') or ''
            author = annot.info.get('title', '') or ''  # author is stored in 'title' field

            # Get highlighted/annotated text
            marked_text = ''
            if annot.type[0] in (8, 9, 10, 11):  # Highlight, Underline, Squiggly, StrikeOut
                try:
                    quads = annot.vertices
                    if quads:
                        rect = fitz.Rect(quads[0], quads[-1])
                        marked_text = page.get_text("text", clip=rect).strip()
                except:
                    pass

            if content or marked_text:
                annotations.append({
                    'page': page_num + 1,
                    'type': annot_type,
                    'comment': content,
                    'marked_text': marked_text,
                    'author': author,
                })

    doc.close()
    return annotations


def parse_word_track_changes(filepath):
    """Extract track changes and comments from a Word document."""
    try:
        from docx import Document
        from lxml import etree
    except ImportError:
        return {'error': 'python-docx and lxml not installed. Run: pip install python-docx lxml --break-system-packages'}

    doc = Document(filepath)
    changes = []
    comments = []

    # Extract comments
    nsmap = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    }

    # Parse comments from the comments part
    try:
        comments_part = doc.part.package.parts
        for part in comments_part:
            if hasattr(part, 'partname') and '/comments.xml' in str(part.partname):
                tree = etree.fromstring(part.blob)
                for comment_el in tree.findall('.//w:comment', nsmap):
                    author = comment_el.get(f'{{{nsmap["w"]}}}author', '')
                    date = comment_el.get(f'{{{nsmap["w"]}}}date', '')
                    text_parts = []
                    for p in comment_el.findall('.//w:t', nsmap):
                        if p.text:
                            text_parts.append(p.text)
                    comment_text = ''.join(text_parts)
                    if comment_text:
                        comments.append({
                            'type': 'comment',
                            'author': author,
                            'date': date,
                            'text': comment_text,
                        })
    except Exception as e:
        pass  # Comments extraction may fail on some docs

    # Extract tracked changes (insertions and deletions) from document body
    body = doc.element.body
    for elem in body.iter():
        tag = etree.QName(elem.tag).localname if isinstance(elem.tag, str) else ''

        if tag == 'ins':
            author = elem.get(f'{{{nsmap["w"]}}}author', '')
            date = elem.get(f'{{{nsmap["w"]}}}date', '')
            text_parts = []
            for t in elem.findall('.//w:t', nsmap):
                if t.text:
                    text_parts.append(t.text)
            if text_parts:
                changes.append({
                    'type': 'insertion',
                    'author': author,
                    'date': date,
                    'text': ''.join(text_parts),
                })

        elif tag == 'del':
            author = elem.get(f'{{{nsmap["w"]}}}author', '')
            date = elem.get(f'{{{nsmap["w"]}}}date', '')
            text_parts = []
            for t in elem.findall('.//w:delText', nsmap):
                if t.text:
                    text_parts.append(t.text)
            if text_parts:
                changes.append({
                    'type': 'deletion',
                    'author': author,
                    'date': date,
                    'text': ''.join(text_parts),
                })

    return {'changes': changes, 'comments': comments}


def parse_reviewer_response(filepath):
    """Parse a reviewer response letter (plain text or simple format)."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Try to detect Q&A pairs
    pairs = []
    # Common patterns: "Reviewer 1:", "Comment:", "Response:", "R1.1:", "Q:", "A:"
    patterns = [
        r'(?:Reviewer\s*\d+.*?(?:Comment|Question)\s*\d*[.:]\s*)(.*?)(?:(?:Author\s*)?Response\s*[.:]\s*)(.*?)(?=Reviewer|Comment|Question|$)',
        r'(?:R\d+[.-]\d+[.:]\s*)(.*?)(?:Response[.:]\s*)(.*?)(?=R\d+|$)',
        r'(?:Q\d*[.:]\s*)(.*?)(?:A\d*[.:]\s*)(.*?)(?=Q\d*|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            for q, a in matches:
                pairs.append({
                    'question': q.strip()[:1000],
                    'response': a.strip()[:1000],
                })
            break

    if not pairs:
        # Fallback: return raw content
        return {'raw_content': content[:5000], 'pairs': []}

    return {'pairs': pairs}


def format_output(all_results, filepath_map):
    """Format all results into readable output."""
    lines = []
    lines.append("# Paper Annotation Parse Results")
    lines.append("")

    for filepath, result in zip(filepath_map, all_results):
        fname = os.path.basename(filepath)
        lines.append(f"## File: {fname}")
        lines.append("")

        if isinstance(result, dict) and 'error' in result:
            lines.append(f"Parse error: {result['error']}")
            lines.append("")
            continue

        # PDF annotations
        if isinstance(result, list):
            lines.append(f"Total annotations: {len(result)}")
            lines.append("")
            for i, annot in enumerate(result[:50], 1):
                lines.append(f"### Annotation {i} (page {annot['page']}, {annot['type']})")
                if annot.get('author'):
                    lines.append(f"Author: {annot['author']}")
                if annot.get('marked_text'):
                    lines.append(f"Marked text: \"{annot['marked_text'][:200]}\"")
                if annot.get('comment'):
                    lines.append(f"Comment: {annot['comment']}")
                lines.append("")

        # Word track changes
        elif isinstance(result, dict) and 'changes' in result:
            changes = result['changes']
            comments = result['comments']
            lines.append(f"Track changes: {len(changes)}")
            lines.append(f"Comments: {len(comments)}")
            lines.append("")

            if comments:
                lines.append("### Comments")
                for i, c in enumerate(comments[:30], 1):
                    lines.append(f"{i}. [{c.get('author', '?')}] {c['text']}")
                lines.append("")

            if changes:
                lines.append("### Track Changes (first 30)")
                for i, ch in enumerate(changes[:30], 1):
                    label = "Insert" if ch['type'] == 'insertion' else "Delete"
                    lines.append(f"{i}. [{label}] [{ch.get('author', '?')}] {ch['text'][:200]}")
                lines.append("")

        # Reviewer response
        elif isinstance(result, dict) and 'pairs' in result:
            pairs = result['pairs']
            if pairs:
                lines.append(f"Reviewer Q&A pairs: {len(pairs)}")
                lines.append("")
                for i, pair in enumerate(pairs[:20], 1):
                    lines.append(f"### Q&A {i}")
                    lines.append(f"**Reviewer comment:** {pair['question'][:500]}")
                    lines.append(f"**Author response:** {pair['response'][:500]}")
                    lines.append("")
            elif result.get('raw_content'):
                lines.append("Could not auto-detect Q&A pairs. Raw content:")
                lines.append(result['raw_content'][:3000])
                lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse paper annotations for mentor skill')
    parser.add_argument('--file', help='Single file to parse')
    parser.add_argument('--dir', help='Directory of files to parse')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    files = []
    if args.file:
        files = [args.file]
    elif args.dir:
        d = Path(args.dir)
        files = sorted(
            [str(f) for f in d.rglob('*')
             if f.suffix.lower() in ('.pdf', '.docx', '.doc', '.txt', '.md')]
        )

    all_results = []
    for fp in files:
        ext = Path(fp).suffix.lower()
        try:
            if ext == '.pdf':
                result = parse_pdf_annotations(fp)
            elif ext in ('.docx', '.doc'):
                result = parse_word_track_changes(fp)
            elif ext in ('.txt', '.md'):
                result = parse_reviewer_response(fp)
            else:
                continue
            all_results.append(result)
        except Exception as e:
            all_results.append({'error': f'Failed to parse: {e}'})

    output_text = format_output(all_results, files)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"Parsed {len(files)} files. Output saved to {args.output}")


if __name__ == '__main__':
    main()
