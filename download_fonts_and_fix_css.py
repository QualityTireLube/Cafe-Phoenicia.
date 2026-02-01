#!/usr/bin/env python3
"""
Download font files and fix CSS references for homepage
"""

import urllib.request
import urllib.parse
import os
import re
import ssl
from pathlib import Path

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SITE_DIR = Path(__file__).parent
ASSETS_DIR = SITE_DIR / 'assets'
FONTS_DIR = ASSETS_DIR / 'fonts'

# Font files to download
FONT_URLS = [
    # FontAwesome fonts
    'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/fonts/fontawesome-webfont.eot',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/fonts/fontawesome-webfont.woff2',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/fonts/fontawesome-webfont.woff',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/fonts/fontawesome-webfont.ttf',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/fonts/fontawesome-webfont.svg',
    # Social icons fonts
    'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/font/social_icons.eot',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/font/social_icons.woff2',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/font/social_icons.woff',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/font/social_icons.ttf',
    'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/font/social_icons.svg',
]

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        print(f"  Downloading: {Path(url).name}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            content = response.read()
            
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, 'wb') as f:
            f.write(content)
        
        print(f"    ✅ Saved: {destination.name}")
        return True
        
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

def fix_css_file(css_path):
    """Fix font URLs in CSS file"""
    print(f"\n  Fixing: {css_path.name}")
    
    with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Fix FontAwesome font paths
    content = re.sub(
        r"url\('https://static\.spotapps\.co/web/cafephoenicia--com/lib/font-awesome-4\.7\.0/css/\.\./fonts/([^']+)'\)",
        r"url('../fonts/\1')",
        content
    )
    
    # Fix social icons font paths
    content = re.sub(
        r"url\('https://static\.spotapps\.co/web/cafephoenicia--com/lib/icons_font/css/\.\./font/([^']+)'\)",
        r"url('../fonts/\1')",
        content
    )
    
    # Fix UIKit font paths
    content = re.sub(
        r"url\('https://static\.spotapps\.co/web/cafephoenicia--com/lib/uikit/css/\.\./fonts/([^']+)'\)",
        r"url('../fonts/\1')",
        content
    )
    
    # Remove Google Fonts import
    content = re.sub(
        r"@import url\(https://fonts\.googleapis\.com/css\?[^)]+\);",
        "/* Google Fonts removed for offline use */",
        content
    )
    
    # Fix other image URLs in style.css
    content = re.sub(
        r"url\('https://static\.spotapps\.co/web/cafephoenicia--com/css/\.\./images/([^']+)'\)",
        r"url('../images/homepage_\1')",
        content
    )
    
    content = re.sub(
        r"url\(https://static\.spotapps\.co/web/cafephoenicia--com/css/\.\./images/([^)]+)\)",
        r"url(../images/homepage_\1)",
        content
    )
    
    if content != original:
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    ✅ Fixed URLs")
    else:
        print(f"    ℹ️  No changes needed")

def main():
    """Download fonts and fix CSS"""
    print("="*60)
    print("📥 DOWNLOADING FONTS & FIXING CSS")
    print("="*60)
    
    # Download fonts
    print("\n📁 FONTS")
    print("-" * 60)
    
    success = 0
    for url in FONT_URLS:
        filename = Path(url).name
        destination = FONTS_DIR / filename
        
        if destination.exists():
            print(f"  ⏭️  Already exists: {filename}")
            success += 1
        elif download_file(url, destination):
            success += 1
    
    print(f"\n  Total: {len(FONT_URLS)}, Downloaded: {success}")
    
    # Fix CSS files
    print("\n📝 FIXING CSS FILES")
    print("-" * 60)
    
    css_files = [
        ASSETS_DIR / 'css' / 'homepage_lib_font-awesome-4.7.0_css_font-awesome.min.css',
        ASSETS_DIR / 'css' / 'homepage_lib_icons_font_css_social_icons.css',
        ASSETS_DIR / 'css' / 'homepage_css_style.css',
        ASSETS_DIR / 'css' / 'homepage_lib_uikit_css_slidenav.css',
    ]
    
    for css_file in css_files:
        if css_file.exists():
            fix_css_file(css_file)
    
    print()
    print("="*60)
    print("✅ COMPLETE!")
    print("="*60)
    print()

if __name__ == "__main__":
    main()
