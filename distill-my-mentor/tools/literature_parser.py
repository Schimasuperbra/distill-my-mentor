#!/usr/bin/env python3
"""
Literature Parser for Mentor Skill
Batch-process PDF papers to extract academic fingerprint.
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


# Common academic stopwords to exclude from term frequency
ACADEMIC_STOPWORDS = {
    'the', 'and', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had',
    'this', 'that', 'with', 'from', 'which', 'also', 'been', 'more', 'than',
    'their', 'these', 'those', 'such', 'into', 'between', 'through', 'during',
    'each', 'other', 'both', 'after', 'before', 'about', 'would', 'could',
    'should', 'will', 'can', 'may', 'might', 'must', 'shall', 'does', 'did',
    'not', 'but', 'only', 'some', 'most', 'very', 'well', 'however', 'although',
    'while', 'where', 'when', 'what', 'how', 'who', 'all', 'any', 'our', 'we',
    'they', 'its', 'using', 'used', 'based', 'one', 'two', 'three',
    # Common academic filler
    'study', 'studies', 'result', 'results', 'figure', 'table', 'fig',
    'show', 'shown', 'shows', 'showed', 'found', 'data', 'analysis',
    'method', 'methods', 'approach', 'paper', 'research', 'work',
    'different', 'important', 'significant', 'significantly', 'effect',
    'effects', 'model', 'models', 'value', 'values', 'number', 'total',
    'first', 'second', 'new', 'high', 'low', 'large', 'small', 'time',
}


def extract_pdf_content(filepath):
    """Extract structured content from a PDF."""
    try:
        import fitz  # pymupdf
    except ImportError:
        return {'error': 'pymupdf not installed. Run: pip install pymupdf --break-system-packages'}

    try:
        doc = fitz.open(filepath)
    except Exception as e:
        return {'error': f'Cannot open PDF: {e}'}

    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"

    # Quality check: use per-page character density instead of absolute length.
    # Scanned PDFs extract < 50 chars/page; real text PDFs are far denser.
    num_pages = doc.page_count
    chars_per_page = len(full_text.strip()) / max(num_pages, 1)

    doc.close()

    if chars_per_page < 50 and len(full_text.strip()) < 200:
        return {'error': f'Extracted text too sparse ({len(full_text.strip())} chars, {num_pages} pages, ~{chars_per_page:.0f} chars/page) — possibly scanned PDF'}

    # Check for garbled text
    ascii_ratio = sum(1 for c in full_text if ord(c) < 128) / max(len(full_text), 1)
    non_printable = sum(1 for c in full_text if not c.isprintable() and c not in '\n\r\t')
    if non_printable / max(len(full_text), 1) > 0.1:
        return {'error': f'High garbled text ratio — possibly scanned PDF or encoding issue'}

    return {'text': full_text, 'char_count': len(full_text)}


def extract_metadata(text):
    """Extract basic metadata from paper text."""
    lines = text.split('\n')
    # Title is usually the first non-empty line (heuristic)
    title = ''
    for line in lines[:10]:
        stripped = line.strip()
        if len(stripped) > 10 and len(stripped) < 300:
            title = stripped
            break

    # Try to find authors (usually after title, before abstract)
    authors = ''
    for line in lines[1:20]:
        stripped = line.strip()
        # Authors often contain commas and are shorter than abstract
        if ',' in stripped and len(stripped) < 500 and not stripped.lower().startswith('abstract'):
            authors = stripped
            break

    # Try to find year
    year = ''
    year_match = re.search(r'20[0-2]\d|19\d\d', text[:3000])
    if year_match:
        year = year_match.group()

    return {'title': title, 'authors': authors, 'year': year}


def extract_sections(text):
    """Extract key sections from paper text."""
    text_lower = text.lower()

    sections = {}

    # Abstract
    abs_patterns = [
        r'(?:^|\n)\s*abstract\s*\n(.*?)(?:\n\s*(?:introduction|keywords|1\s|1\.))',
        r'(?:^|\n)\s*abstract[.:]\s*(.*?)(?:\n\s*(?:introduction|keywords|1\s|1\.))',
    ]
    for pat in abs_patterns:
        match = re.search(pat, text_lower, re.DOTALL)
        if match:
            start = match.start(1)
            sections['abstract'] = text[start:start + len(match.group(1))].strip()[:2000]
            break

    # Introduction (first 2000 chars after header)
    intro_match = re.search(
        r'(?:^|\n)\s*(?:1\.?\s+)?introduction\s*\n',
        text_lower
    )
    if intro_match:
        start = intro_match.end()
        sections['introduction'] = text[start:start + 3000].strip()

    # Discussion/Conclusion (last major section)
    disc_patterns = [
        r'(?:^|\n)\s*(?:\d+\.?\s+)?(?:discussion|conclusions?|discussion and conclusions?)\s*\n',
    ]
    for pat in disc_patterns:
        matches = list(re.finditer(pat, text_lower))
        if matches:
            start = matches[-1].end()
            sections['discussion'] = text[start:start + 3000].strip()
            break

    # Methods
    meth_match = re.search(
        r'(?:^|\n)\s*(?:\d+\.?\s+)?(?:method(?:s|ology)?|materials?\s+and\s+methods?|experimental)\s*\n',
        text_lower
    )
    if meth_match:
        start = meth_match.end()
        sections['methods'] = text[start:start + 2000].strip()

    return sections


def compute_term_frequency(text, top_n=30):
    """Compute term frequency excluding stopwords."""
    # Tokenize: split on non-alphanumeric, keep words 3+ chars
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    # Also capture common multi-word terms
    bigrams = []
    for i in range(len(words) - 1):
        bg = f"{words[i]} {words[i+1]}"
        bigrams.append(bg)

    word_counts = Counter(w for w in words if w not in ACADEMIC_STOPWORDS)
    bigram_counts = Counter(bg for bg in bigrams
                           if all(w not in ACADEMIC_STOPWORDS for w in bg.split()))

    # Merge: prefer bigrams if they appear 5+ times
    merged = dict(word_counts.most_common(top_n * 2))
    for bg, count in bigram_counts.most_common(top_n):
        if count >= 5:
            merged[bg] = count

    return sorted(merged.items(), key=lambda x: -x[1])[:top_n]


def check_is_mentor_paper(authors_text, mentor_name):
    """Check if the mentor is in the author list."""
    if not mentor_name or not authors_text:
        return False
    # Normalize
    name_parts = mentor_name.lower().split()
    authors_lower = authors_text.lower()
    # Check if any name part (especially surname) appears
    # This is a heuristic — surname matching
    if len(name_parts) >= 2:
        surname = name_parts[-1]
        if len(surname) > 2 and surname in authors_lower:
            return True
    # Full name match
    if mentor_name.lower() in authors_lower:
        return True
    return False


def process_paper(filepath, mentor_name):
    """Process a single PDF paper."""
    content = extract_pdf_content(filepath)
    if 'error' in content:
        return {'file': os.path.basename(filepath), 'error': content['error']}

    text = content['text']
    metadata = extract_metadata(text)
    sections = extract_sections(text)
    terms = compute_term_frequency(text, top_n=20)
    is_mentor = check_is_mentor_paper(metadata.get('authors', ''), mentor_name)

    return {
        'file': os.path.basename(filepath),
        'title': metadata.get('title', ''),
        'authors': metadata.get('authors', ''),
        'year': metadata.get('year', ''),
        'is_mentor_paper': is_mentor,
        'char_count': content['char_count'],
        'sections': {k: v[:2000] for k, v in sections.items()},
        'top_terms': terms[:20],
    }


def format_output(papers):
    """Format results into readable text."""
    lines = []
    lines.append("# Literature Parse Results")
    lines.append("")

    mentor_papers = [p for p in papers if not p.get('error') and p.get('is_mentor_paper')]
    other_papers = [p for p in papers if not p.get('error') and not p.get('is_mentor_paper')]
    failed = [p for p in papers if p.get('error')]

    lines.append(f"Successfully parsed: {len(mentor_papers) + len(other_papers)} papers")
    lines.append(f"  Mentor papers: {len(mentor_papers)}")
    lines.append(f"  Recommended literature: {len(other_papers)}")
    lines.append(f"Failed to parse: {len(failed)}")
    lines.append("")

    if failed:
        lines.append("## Failed Files")
        for p in failed:
            lines.append(f"- {p['file']}: {p['error']}")
        lines.append("")

    # Aggregate term frequency across all mentor papers
    if mentor_papers:
        all_terms = Counter()
        for p in mentor_papers:
            for term, count in p.get('top_terms', []):
                all_terms[term] += count

        lines.append("## Mentor Papers — Aggregated Top Terms (Top 30)")
        for term, count in all_terms.most_common(30):
            lines.append(f"- \"{term}\": {count}x")
        lines.append("")

    # Individual papers
    for label, paper_list in [("Mentor Papers", mentor_papers), ("Recommended Literature", other_papers)]:
        if not paper_list:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for p in paper_list:
            lines.append(f"### {p.get('title', p['file'])}")
            lines.append(f"- File: {p['file']}")
            lines.append(f"- Year: {p.get('year', '?')}")
            lines.append(f"- Authors: {p.get('authors', '?')[:200]}")
            lines.append(f"- Char count: {p.get('char_count', '?')}")
            lines.append("")

            secs = p.get('sections', {})
            if 'abstract' in secs:
                lines.append("**Abstract:**")
                lines.append(secs['abstract'][:1500])
                lines.append("")
            if 'introduction' in secs:
                lines.append("**Introduction (excerpt):**")
                lines.append(secs['introduction'][:1500])
                lines.append("")
            if 'discussion' in secs:
                lines.append("**Discussion (excerpt):**")
                lines.append(secs['discussion'][:1500])
                lines.append("")
            if 'methods' in secs:
                lines.append("**Methods (excerpt):**")
                lines.append(secs['methods'][:1000])
                lines.append("")

            lines.append("**Top terms:**")
            for term, count in p.get('top_terms', [])[:10]:
                lines.append(f"  - \"{term}\": {count}x")
            lines.append("")
            lines.append("---")
            lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse literature PDFs for mentor skill')
    parser.add_argument('--dir', required=True, help='Directory containing PDF files')
    parser.add_argument('--mentor-name', default='', help='Mentor name for author matching')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    pdf_dir = Path(args.dir)
    pdf_files = sorted(pdf_dir.rglob('*.pdf'))

    if not pdf_files:
        print(f"No PDF files found in {args.dir}")
        with open(args.output, 'w') as f:
            f.write("# Literature Parse Results\n\nNo PDF files found.\n")
        return

    print(f"Found {len(pdf_files)} PDF files. Processing...")

    papers = []
    for i, fp in enumerate(pdf_files, 1):
        print(f"  [{i}/{len(pdf_files)}] {fp.name}")
        result = process_paper(str(fp), args.mentor_name)
        papers.append(result)

    output_text = format_output(papers)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"Done. Output saved to {args.output}")


if __name__ == '__main__':
    main()
