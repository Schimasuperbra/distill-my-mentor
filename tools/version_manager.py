#!/usr/bin/env python3
"""
Version Manager for Mentor Skill
Handles version archiving, listing, and rollback of generated mentor Skills.
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


VERSIONED_FILES = [
    'SKILL.md',
    'guidance.md',
    'style.md',
    'thinking_framework.md',
    'meta.json',
]


def save_version(base_dir, slug):
    """Archive the current version of a mentor skill."""
    mentor_dir = Path(base_dir) / slug
    versions_dir = mentor_dir / 'versions'
    versions_dir.mkdir(parents=True, exist_ok=True)

    # Read current version number
    meta_path = mentor_dir / 'meta.json'
    version = 1
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        version = meta.get('version', 1)

    # Create version directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_label = f"v{version}_{timestamp}"
    version_dir = versions_dir / version_label
    version_dir.mkdir(parents=True, exist_ok=True)

    # Copy versioned files
    copied = []
    for fname in VERSIONED_FILES:
        src = mentor_dir / fname
        if src.exists():
            shutil.copy2(str(src), str(version_dir / fname))
            copied.append(fname)

    # Write version manifest
    manifest = {
        'version': version,
        'label': version_label,
        'timestamp': datetime.now().isoformat(),
        'files': copied,
    }
    with open(version_dir / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Increment version in meta.json so the next save gets a new version label
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        meta['version'] = meta.get('version', 1) + 1
        meta['updated_at'] = datetime.now().isoformat()
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Saved version {version_label} ({len(copied)} files)")
    return version_label


def list_versions(base_dir, slug):
    """List all versions of a mentor skill."""
    versions_dir = Path(base_dir) / slug / 'versions'
    if not versions_dir.exists():
        print("No versions found.")
        return []

    versions = []
    for d in sorted(versions_dir.iterdir()):
        manifest_path = d / 'manifest.json'
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            versions.append(manifest)
            print(f"  {manifest['label']} | {manifest['timestamp']} | {len(manifest['files'])} files")

    if not versions:
        print("No versions found.")
    return versions


def rollback(base_dir, slug, version_label):
    """Rollback a mentor skill to a previous version."""
    mentor_dir = Path(base_dir) / slug
    version_dir = mentor_dir / 'versions' / version_label

    if not version_dir.exists():
        # Try partial match
        versions_dir = mentor_dir / 'versions'
        matches = [d for d in versions_dir.iterdir() if version_label in d.name]
        if len(matches) == 1:
            version_dir = matches[0]
        elif len(matches) > 1:
            print(f"Ambiguous version label '{version_label}'. Matches: {[m.name for m in matches]}")
            return False
        else:
            print(f"Version '{version_label}' not found.")
            return False

    # Save current state before rollback
    print("Saving current state before rollback...")
    save_version(base_dir, slug)

    # Restore files from version
    restored = []
    for fname in VERSIONED_FILES:
        src = version_dir / fname
        dst = mentor_dir / fname
        if src.exists():
            shutil.copy2(str(src), str(dst))
            restored.append(fname)

    print(f"Rolled back to {version_dir.name} ({len(restored)} files restored)")
    return True


def main():
    parser = argparse.ArgumentParser(description='Manage mentor skill versions')
    parser.add_argument('--action', required=True,
                        choices=['save', 'list', 'rollback'],
                        help='Action to perform')
    parser.add_argument('--base-dir', default='./mentors', help='Base directory')
    parser.add_argument('--slug', required=True, help='Mentor slug')
    parser.add_argument('--version', help='Version label (for rollback)')

    args = parser.parse_args()

    if args.action == 'save':
        save_version(args.base_dir, args.slug)
    elif args.action == 'list':
        list_versions(args.base_dir, args.slug)
    elif args.action == 'rollback':
        if not args.version:
            print("Error: --version is required for rollback")
            return
        rollback(args.base_dir, args.slug, args.version)


if __name__ == '__main__':
    main()
