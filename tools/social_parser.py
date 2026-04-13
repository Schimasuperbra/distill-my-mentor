#!/usr/bin/env python3
"""
Social Media Parser for Mentor Skill
Parses social media exports (Weibo, Xiaohongshu, Douban, Instagram, generic text/JSON).
"""

import argparse
import json
import re
from pathlib import Path


def parse_json_export(filepath, target_name, platform):
    """Parse JSON exports from various social media platforms."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    
    posts = []
    
    # Handle different JSON structures
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # Try common keys
        for key in ['data', 'posts', 'items', 'statuses', 'notes', 'entries']:
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
        if not items:
            items = [data]
    
    for item in items:
        if not isinstance(item, dict):
            continue
        
        # Extract content from common field names
        content = ''
        for key in ['text', 'content', 'body', 'desc', 'description', 'note', 'message', 'status_text']:
            if key in item and isinstance(item[key], str):
                content = item[key]
                break
        
        # Extract timestamp
        timestamp = ''
        for key in ['created_at', 'time', 'date', 'timestamp', 'publish_time', 'create_time']:
            if key in item:
                timestamp = str(item[key])
                break
        
        # Extract author
        author = ''
        if 'user' in item and isinstance(item['user'], dict):
            author = item['user'].get('name', item['user'].get('screen_name', ''))
        for key in ['author', 'nickname', 'username', 'screen_name']:
            if key in item and isinstance(item[key], str):
                author = item[key]
                break
        
        if content:
            posts.append({
                'content': content,
                'timestamp': timestamp,
                'author': author,
                'platform': platform,
            })
    
    return posts


def parse_text_export(filepath, target_name, platform):
    """Parse plain text or copied social media content."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Try to split into individual posts
    # Common separators: double newlines, horizontal rules, timestamps
    posts = []
    
    # Split by double newlines or horizontal rules
    chunks = re.split(r'\n\s*\n|\n-{3,}\n|\n={3,}\n', content)
    
    for chunk in chunks:
        chunk = chunk.strip()
        if len(chunk) < 10:
            continue
        posts.append({
            'content': chunk,
            'timestamp': '',
            'author': target_name or '',
            'platform': platform,
        })
    
    if not posts and content.strip():
        posts.append({
            'content': content.strip(),
            'timestamp': '',
            'author': target_name or '',
            'platform': platform,
        })
    
    return posts


def filter_mentor_posts(posts, target_name):
    """Filter posts to only include those by the mentor."""
    if not target_name:
        return posts
    
    target_lower = target_name.lower()
    filtered = []
    for post in posts:
        author = post.get('author', '').lower()
        if not author or target_lower in author or author in target_lower:
            filtered.append(post)
    
    return filtered if filtered else posts


def format_output(posts, target_name, platform):
    """Format results."""
    lines = []
    lines.append("# Social Media Content Parse Results")
    lines.append("")
    lines.append(f"Target mentor: {target_name}")
    lines.append(f"Platform: {platform}")
    lines.append(f"Posts/items: {len(posts)}")
    lines.append("")
    
    for i, post in enumerate(posts[:50], 1):
        lines.append(f"## Post {i}")
        if post.get('timestamp'):
            lines.append(f"Time: {post['timestamp']}")
        if post.get('author'):
            lines.append(f"Author: {post['author']}")
        lines.append("Content:")
        lines.append(post['content'][:1000])
        if len(post['content']) > 1000:
            lines.append(f"... (truncated, total {len(post['content'])} chars)")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse social media content for mentor skill')
    parser.add_argument('--file', required=True, help='Social media export file or directory')
    parser.add_argument('--platform', default='generic',
                        choices=['weibo', 'douban', 'xiaohongshu', 'instagram', 'twitter', 'text', 'generic'],
                        help='Platform type')
    parser.add_argument('--target', default='', help='Mentor name to filter posts')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()
    
    filepath = Path(args.file)
    all_posts = []
    
    files_to_parse = []
    if filepath.is_dir():
        files_to_parse = sorted(filepath.rglob('*'))
    else:
        files_to_parse = [filepath]
    
    for fp in files_to_parse:
        if not fp.is_file():
            continue
        try:
            if fp.suffix.lower() == '.json':
                posts = parse_json_export(str(fp), args.target, args.platform)
            elif fp.suffix.lower() in ('.txt', '.text', '.md', '.html', '.htm', '.csv'):
                posts = parse_text_export(str(fp), args.target, args.platform)
            else:
                continue
            all_posts.extend(posts)
        except Exception as e:
            print(f"Warning: Failed to parse {fp}: {e}")
    
    all_posts = filter_mentor_posts(all_posts, args.target)
    output_text = format_output(all_posts, args.target, args.platform)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"Parsed {len(all_posts)} posts. Output saved to {args.output}")


if __name__ == '__main__':
    main()
