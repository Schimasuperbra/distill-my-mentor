#!/usr/bin/env python3
"""
Photo Analyzer for Mentor Skill
Extracts EXIF metadata from photos to build a timeline.
"""

import argparse
import os
import json
from pathlib import Path
from datetime import datetime


def extract_exif(filepath):
    """Extract EXIF data from an image file."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
    except ImportError:
        return {'error': 'Pillow not installed. Run: pip install Pillow --break-system-packages'}
    
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
    except Exception as e:
        return {'error': f'Cannot read EXIF: {e}'}
    
    if not exif_data:
        return {'error': 'No EXIF data found'}
    
    result = {}
    
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, str(tag_id))
        
        if tag_name == 'DateTimeOriginal':
            result['datetime'] = str(value)
        elif tag_name == 'DateTime':
            if 'datetime' not in result:
                result['datetime'] = str(value)
        elif tag_name == 'Make':
            result['camera_make'] = str(value)
        elif tag_name == 'Model':
            result['camera_model'] = str(value)
        elif tag_name == 'GPSInfo':
            gps = {}
            for gps_tag_id, gps_value in value.items():
                gps_tag = GPSTAGS.get(gps_tag_id, str(gps_tag_id))
                gps[gps_tag] = gps_value
            
            # Convert GPS coordinates to decimal
            try:
                lat = _gps_to_decimal(gps.get('GPSLatitude'), gps.get('GPSLatitudeRef'))
                lon = _gps_to_decimal(gps.get('GPSLongitude'), gps.get('GPSLongitudeRef'))
                if lat and lon:
                    result['gps_lat'] = lat
                    result['gps_lon'] = lon
            except:
                pass
    
    result['filename'] = os.path.basename(filepath)
    return result


def _gps_to_decimal(coords, ref):
    """Convert GPS coordinates from DMS to decimal."""
    if not coords or not ref:
        return None
    
    try:
        if isinstance(coords[0], tuple):
            d = coords[0][0] / coords[0][1]
            m = coords[1][0] / coords[1][1]
            s = coords[2][0] / coords[2][1]
        else:
            d = float(coords[0])
            m = float(coords[1])
            s = float(coords[2])
        
        decimal = d + m / 60 + s / 3600
        if ref in ('S', 'W'):
            decimal = -decimal
        return round(decimal, 6)
    except:
        return None


def build_timeline(photos):
    """Build a chronological timeline from photo metadata."""
    dated = []
    undated = []
    
    for photo in photos:
        if 'error' in photo:
            continue
        if 'datetime' in photo:
            dated.append(photo)
        else:
            undated.append(photo)
    
    # Sort by datetime
    def parse_dt(dt_str):
        for fmt in ['%Y:%m:%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return datetime.min
    
    dated.sort(key=lambda p: parse_dt(p.get('datetime', '')))
    
    return dated, undated


def format_output(dated, undated, total_files):
    """Format results."""
    lines = []
    lines.append("# Photo Timeline Analysis")
    lines.append("")
    lines.append(f"Files scanned: {total_files}")
    lines.append(f"Photos with EXIF date: {len(dated)}")
    lines.append(f"Photos without EXIF date: {len(undated)}")
    lines.append("")
    
    if dated:
        lines.append("## Timeline")
        lines.append("")
        
        current_month = ""
        for photo in dated:
            dt = photo.get('datetime', '')
            month = dt[:7].replace(':', '-') if len(dt) >= 7 else 'unknown'
            
            if month != current_month:
                current_month = month
                lines.append(f"### {current_month}")
            
            location = ""
            if 'gps_lat' in photo and 'gps_lon' in photo:
                location = f" | GPS: ({photo['gps_lat']}, {photo['gps_lon']})"
            
            camera = ""
            if 'camera_model' in photo:
                camera = f" | Camera: {photo['camera_model']}"
            
            lines.append(f"- {photo['filename']} | {dt}{location}{camera}")
        
        lines.append("")
    
    if undated:
        lines.append("## Photos Without Date")
        for photo in undated:
            lines.append(f"- {photo.get('filename', '?')}")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Analyze photo EXIF for mentor skill')
    parser.add_argument('--dir', required=True, help='Directory containing photos')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()
    
    photo_dir = Path(args.dir)
    extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.heic', '.heif'}
    
    photo_files = sorted(
        f for f in photo_dir.rglob('*')
        if f.suffix.lower() in extensions
    )
    
    if not photo_files:
        with open(args.output, 'w') as f:
            f.write("# Photo Timeline Analysis\n\nNo image files found.\n")
        print("No photo files found.")
        return
    
    print(f"Found {len(photo_files)} photos. Processing...")
    
    photos = []
    for fp in photo_files:
        result = extract_exif(str(fp))
        if 'error' in result and 'Pillow' in result['error']:
            print(f"Error: {result['error']}")
            with open(args.output, 'w') as f:
                f.write(f"# Photo Timeline Analysis\n\n{result['error']}\n")
            return
        photos.append(result)
    
    dated, undated = build_timeline(photos)
    output_text = format_output(dated, undated, len(photo_files))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"Processed {len(photo_files)} photos. Output saved to {args.output}")


if __name__ == '__main__':
    main()
