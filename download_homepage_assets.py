#!/usr/bin/env python3
"""
Download all assets for the Cafe Phoenicia homepage
This script downloads CSS, JS, images from the original site
"""

import urllib.request
import urllib.parse
import os
import re
import ssl
from pathlib import Path

# Create SSL context that doesn't verify certificates (for development)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SITE_DIR = Path(__file__).parent
ASSETS_DIR = SITE_DIR / 'assets'

# Asset URLs from the original page
ASSETS_TO_DOWNLOAD = {
    'css': [
        'https://static.spotapps.co/web/cafephoenicia--com/lib/bootstrap/css/bootstrap.min.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/gallery/gallery.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/fancybox/source/jquery.fancybox.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/fancybox/source/helpers/jquery.fancybox-thumbs.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/uikit/css/uikit.docs.min.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/uikit/css/slidenav.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/font-awesome-4.7.0/css/font-awesome.min.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/hover_css/css/hover-min.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/owlcarousel/owl.carousel.min.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/owlcarousel/owl.theme.default.min.css',
        'https://static.spotapps.co/web-lib/leaflet/leaflet@1.3.1/dist/leaflet.css',
        'https://static.spotapps.co/web/cafephoenicia--com/css/style.css',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/icons_font/css/social_icons.css',
    ],
    'js': [
        'https://static.spotapps.co/web/cafephoenicia--com/lib/jquery/jquery.min.js',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/jquery/jquery.browser.min.js',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/bootstrap/js/bootstrap.min.js',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/owlcarousel/owl.carousel.min.js',
        'https://static.spotapps.co/web/cafephoenicia--com/lib/masonry/masonry.pkgd.min.js',
        'https://static.spotapps.co/slideshow_and_video_control_buttons_mt_plugin_v2.js',
    ],
    'images': [
        'https://static.spotapps.co/web/cafephoenicia--com/custom/logo.png',
        'https://static.spotapps.co/web/cafephoenicia--com/apple-touch-icon.png',
        'https://static.spotapps.co/web/cafephoenicia--com/favicon-32x32.png',
        'https://static.spotapps.co/web/cafephoenicia--com/favicon-16x16.png',
    ]
}

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        print(f"  Downloading: {url}")
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

def get_local_path(url, asset_type):
    """Convert URL to local path"""
    # Parse URL
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    
    # Extract filename
    filename = Path(path).name
    
    # Handle specific cases
    if 'cafephoenicia--com' in url:
        # Extract the path after cafephoenicia--com
        parts = path.split('cafephoenicia--com/')
        if len(parts) > 1:
            subpath = parts[1]
            # Clean up the path
            clean_path = subpath.replace('/', '_')
            filename = f"homepage_{clean_path}"
    elif 'leaflet' in url:
        filename = f"leaflet_{Path(path).name}"
    
    # Determine subdirectory
    if asset_type == 'css':
        return ASSETS_DIR / 'css' / filename
    elif asset_type == 'js':
        return ASSETS_DIR / 'js' / filename
    elif asset_type == 'images':
        return ASSETS_DIR / 'images' / filename
    
    return ASSETS_DIR / asset_type / filename

def main():
    """Download all homepage assets"""
    print("="*60)
    print("📥 DOWNLOADING HOMEPAGE ASSETS")
    print("="*60)
    print()
    
    total = 0
    success = 0
    
    for asset_type, urls in ASSETS_TO_DOWNLOAD.items():
        print(f"\n📁 {asset_type.upper()}")
        print("-" * 60)
        
        for url in urls:
            total += 1
            local_path = get_local_path(url, asset_type)
            
            # Skip if already exists
            if local_path.exists():
                print(f"  ⏭️  Already exists: {local_path.name}")
                success += 1
                continue
            
            if download_file(url, local_path):
                success += 1
    
    print()
    print("="*60)
    print("✅ DOWNLOAD COMPLETE!")
    print("="*60)
    print(f"Total files: {total}")
    print(f"Downloaded: {success}")
    print(f"Failed: {total - success}")
    print()

if __name__ == "__main__":
    main()
