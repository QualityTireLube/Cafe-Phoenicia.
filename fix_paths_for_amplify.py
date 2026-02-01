#!/usr/bin/env python3
"""
Fix asset paths for AWS Amplify deployment
This script ensures all subdirectory pages use correct relative paths
"""

import os
import re
from pathlib import Path

SITE_DIR = Path(__file__).parent

# Subdirectories that need path fixes
SUBDIRS = ['central', 'zachary', 'denhamsprings']

def fix_paths_in_file(file_path):
    """Fix asset paths in a single HTML file"""
    print(f"Fixing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # Fix paths that should be relative to parent directory
    # href="assets/ -> href="../assets/
    # src="assets/ -> src="../assets/
    
    # But NOT if they already have ../ prefix
    patterns = [
        (r'href="assets/', r'href="../assets/'),
        (r"href='assets/", r"href='../assets/"),
        (r'src="assets/', r'src="../assets/'),
        (r"src='assets/", r"src='../assets/"),
    ]
    
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes += len(re.findall(pattern, content))
            content = new_content
    
    # Fix the css/custom.css reference (should be removed or point to assets)
    content = re.sub(r'href="css/custom\.css[^"]*"', r'href="../assets/css/custom_cafephoenicia.css"', content)
    content = re.sub(r"href='css/custom\.css[^']*'", r"href='../assets/css/custom_cafephoenicia.css'", content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Fixed {changes} paths")
        return True
    else:
        print(f"  ℹ️  No changes needed")
        return False

def main():
    """Fix paths in all subdirectory HTML files"""
    print("="*60)
    print("🔧 FIXING ASSET PATHS FOR AWS AMPLIFY")
    print("="*60)
    print()
    
    total_files = 0
    total_fixed = 0
    
    for subdir in SUBDIRS:
        subdir_path = SITE_DIR / subdir
        
        if not subdir_path.exists():
            print(f"⚠️  Directory not found: {subdir}")
            continue
        
        print(f"\n📁 Processing: {subdir}/")
        print("-" * 60)
        
        html_files = list(subdir_path.glob('*.html'))
        
        for html_file in html_files:
            total_files += 1
            if fix_paths_in_file(html_file):
                total_fixed += 1
    
    print()
    print("="*60)
    print("✅ PATH FIXING COMPLETE!")
    print("="*60)
    print(f"Files processed: {total_files}")
    print(f"Files fixed: {total_fixed}")
    print()
    
    if total_fixed > 0:
        print("🎉 Asset paths have been corrected!")
        print("   All subdirectory pages now use '../assets/' paths")
        print()
        print("📤 Next steps:")
        print("   1. Test locally: open central/index.html in browser")
        print("   2. Commit changes: git add . && git commit -m 'Fix asset paths'")
        print("   3. Push to Git: git push")
        print("   4. AWS Amplify will auto-deploy with correct paths!")
    else:
        print("ℹ️  All paths are already correct!")
    
    print()

if __name__ == "__main__":
    main()
