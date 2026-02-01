#!/usr/bin/env python3
"""
Update all internal links to remove .html extensions
This makes URLs cleaner: /central/food-menu instead of /central/food-menu.html
"""

import re
from pathlib import Path

SITE_DIR = Path(__file__).parent
SUBDIRS = ['central', 'zachary', 'denhamsprings']

def update_links_in_file(file_path):
    """Remove .html from internal links in a file"""
    print(f"Processing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # Pattern to match internal links ending with .html
    # This will match: href="food-menu.html", href="index.html", href="../central/food-menu.html"
    # But NOT external links or asset links
    
    # Match relative links within same directory
    pattern1 = r'href="([a-zA-Z0-9\-_]+)\.html"'
    replacement1 = r'href="\1"'
    new_content = re.sub(pattern1, replacement1, content)
    changes += len(re.findall(pattern1, content))
    content = new_content
    
    # Match links to subdirectories
    pattern2 = r'href="\.\./([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-_]+)\.html"'
    replacement2 = r'href="../\1/\2"'
    new_content = re.sub(pattern2, replacement2, content)
    changes += len(re.findall(pattern2, content))
    content = new_content
    
    # Match links within subdirectories (from homepage)
    pattern3 = r'href="([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-_]+)\.html"'
    replacement3 = r'href="\1/\2"'
    new_content = re.sub(pattern3, replacement3, content)
    changes += len(re.findall(pattern3, content))
    content = new_content
    
    # Special case: index.html links
    # href="index.html" -> href="./" or href=""
    content = re.sub(r'href="index\.html"', r'href="./"', content)
    content = re.sub(r'href="\.\./([a-zA-Z0-9\-_]+)/index\.html"', r'href="../\1/"', content)
    content = re.sub(r'href="([a-zA-Z0-9\-_]+)/index\.html"', r'href="\1/"', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated {changes} links")
        return True
    else:
        print(f"  ℹ️  No changes needed")
        return False

def main():
    """Update links in all HTML files"""
    print("="*60)
    print("🔗 UPDATING INTERNAL LINKS - REMOVING .HTML")
    print("="*60)
    print()
    
    total_files = 0
    total_updated = 0
    
    # Update homepage
    print("📄 Homepage")
    print("-" * 60)
    homepage = SITE_DIR / 'index.html'
    if homepage.exists():
        total_files += 1
        if update_links_in_file(homepage):
            total_updated += 1
    
    # Update subdirectory pages
    for subdir in SUBDIRS:
        subdir_path = SITE_DIR / subdir
        
        if not subdir_path.exists():
            print(f"⚠️  Directory not found: {subdir}")
            continue
        
        print(f"\n📁 {subdir.upper()}")
        print("-" * 60)
        
        html_files = list(subdir_path.glob('*.html'))
        
        for html_file in html_files:
            total_files += 1
            if update_links_in_file(html_file):
                total_updated += 1
    
    print()
    print("="*60)
    print("✅ LINK UPDATE COMPLETE!")
    print("="*60)
    print(f"Files processed: {total_files}")
    print(f"Files updated: {total_updated}")
    print()
    
    if total_updated > 0:
        print("🎉 Internal links updated!")
        print("   URLs will now appear without .html extension")
        print()
        print("📤 Next steps:")
        print("   1. Test locally with a server that supports URL rewriting")
        print("   2. Commit changes: git add . && git commit -m 'Remove .html from URLs'")
        print("   3. Push to AWS Amplify: git push")
        print("   4. Amplify will handle URL rewriting automatically!")
    else:
        print("ℹ️  All links already clean!")
    
    print()

if __name__ == "__main__":
    main()
