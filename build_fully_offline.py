#!/usr/bin/env python3
"""
Enhanced Offline Site Builder for Cafe Phoenicia
This script makes the site completely self-contained with NO external dependencies.
"""

import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
import ssl
import shutil
import hashlib

# Configuration
SITE_DIR = Path(__file__).parent
ASSETS_DIR = SITE_DIR / "assets"
CSS_DIR = ASSETS_DIR / "css"
JS_DIR = ASSETS_DIR / "js"
IMAGES_DIR = ASSETS_DIR / "images"
FONTS_DIR = ASSETS_DIR / "fonts"

# Create directories
for d in [ASSETS_DIR, CSS_DIR, JS_DIR, IMAGES_DIR, FONTS_DIR]:
    d.mkdir(exist_ok=True)

# SSL context for downloads
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Track downloaded assets
downloaded_assets = {}

# Location subdomains
LOCATIONS = {
    'central': {
        'source_dir': SITE_DIR / 'central.cafephoenicia.com',
        'output_dir': SITE_DIR / 'central',
        'domain': 'central.cafephoenicia.com',
    },
    'denhamsprings': {
        'source_dir': SITE_DIR / 'denhamsprings.cafephoenicia.com',
        'output_dir': SITE_DIR / 'denhamsprings',
        'domain': 'denhamsprings.cafephoenicia.com',
    },
    'zachary': {
        'source_dir': SITE_DIR / 'zachary.cafephoenicia.com',
        'output_dir': SITE_DIR / 'zachary',
        'domain': 'zachary.cafephoenicia.com',
    }
}

def get_safe_filename(url):
    """Convert URL to safe local filename."""
    # Create hash for very long URLs
    if len(url) > 200:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        parsed = urllib.parse.urlparse(url)
        ext = Path(parsed.path).suffix or '.file'
        return f"asset_{url_hash}{ext}"
    
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    
    # Remove leading slash and replace remaining slashes
    filename = path.lstrip('/').replace('/', '_')
    
    # Handle query strings for cache-busted files
    if '?' in filename:
        base = filename.split('?')[0]
        if base:
            filename = base
    
    # Ensure we have an extension
    if not any(filename.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.ico', '.m4v', '.mp4']):
        if 'css' in url.lower() or 'font' in url.lower():
            filename += '.css'
        elif 'js' in url.lower() or 'javascript' in url.lower():
            filename += '.js'
        elif any(img in url.lower() for img in ['image', 'img', 'photo', 'logo', 'icon']):
            filename += '.jpg'
    
    # Clean up filename
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    
    return filename

def download_asset(url, asset_type='images', force_type=None):
    """Download an asset and return local path."""
    if url in downloaded_assets:
        return downloaded_assets[url]
    
    # Skip data URIs
    if url.startswith('data:'):
        return url
    
    # Skip empty or invalid URLs
    if not url or url == '#' or url.startswith('javascript:'):
        return url
    
    # Determine target directory based on force_type or asset_type
    target_type = force_type or asset_type
    
    if target_type == 'css' or '.css' in url:
        target_dir = CSS_DIR
        rel_path = 'assets/css'
    elif target_type == 'js' or '.js' in url:
        target_dir = JS_DIR
        rel_path = 'assets/js'
    elif any(ext in url.lower() for ext in ['.woff', '.woff2', '.ttf', '.eot', '.otf']):
        target_dir = FONTS_DIR
        rel_path = 'assets/fonts'
    elif any(ext in url.lower() for ext in ['.m4v', '.mp4', '.webm']):
        target_dir = ASSETS_DIR / 'videos'
        target_dir.mkdir(exist_ok=True)
        rel_path = 'assets/videos'
    else:
        target_dir = IMAGES_DIR
        rel_path = 'assets/images'
    
    filename = get_safe_filename(url)
    if not filename:
        return url
        
    local_path = target_dir / filename
    relative_path = f"{rel_path}/{filename}"
    
    # Make URL absolute if needed
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        # Skip relative URLs that don't have a domain
        return url
    
    # Download if not already downloaded
    if not local_path.exists():
        try:
            print(f"Downloading: {url}")
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                content = response.read()
                with open(local_path, 'wb') as f:
                    f.write(content)
            print(f"  -> Saved: {relative_path}")
        except Exception as e:
            print(f"  -> Failed to download {url}: {e}")
            return url
    else:
        print(f"  -> Already exists: {relative_path}")
    
    downloaded_assets[url] = relative_path
    return relative_path

def extract_all_external_resources(html_content):
    """Extract ALL external resources from HTML."""
    resources = {
        'css': set(),
        'js': set(),
        'images': set(),
        'fonts': set(),
        'videos': set()
    }
    
    # CSS files - catch ALL href patterns
    css_patterns = [
        r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet["\']',
        r'rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']',
        r'href=["\']([^"\']*https?://[^"\']+\.css[^"\']*)["\']',
    ]
    for pattern in css_patterns:
        for match in re.findall(pattern, html_content, re.IGNORECASE):
            if match and not match.startswith('data:'):
                resources['css'].add(match)
    
    # JavaScript files
    js_patterns = [
        r'<script[^>]+src=["\']([^"\']+)["\']',
        r'src=["\']([^"\']*https?://[^"\']+\.js[^"\']*)["\']',
    ]
    for pattern in js_patterns:
        for match in re.findall(pattern, html_content, re.IGNORECASE):
            if match and not match.startswith('data:'):
                resources['js'].add(match)
    
    # Images - all formats
    img_patterns = [
        r'<img[^>]+src=["\']([^"\']+)["\']',
        r'<source[^>]+src=["\']([^"\']+)["\']',
        r'data-src=["\']([^"\']+\.(png|jpg|jpeg|gif|webp|svg|ico)[^"\']*)["\']',
        r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)',
        r'content=["\']([^"\']+\.(png|jpg|jpeg|gif|webp|svg|ico)[^"\']*)["\']',
        r'href=["\']([^"\']+\.(png|ico)[^"\']*)["\']',
        r'url\(["\']?([^"\')\s]+\.(png|jpg|jpeg|gif|webp|svg))["\']?\)',
    ]
    for pattern in img_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if match and not match.startswith('data:') and not match.startswith('javascript:'):
                resources['images'].add(match)
    
    # Videos
    video_patterns = [
        r'<video[^>]+src=["\']([^"\']+)["\']',
        r'<source[^>]+src=["\']([^"\']+\.(mp4|m4v|webm)[^"\']*)["\']',
    ]
    for pattern in video_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if match:
                resources['videos'].add(match)
    
    # Font files from CSS @font-face or direct links
    font_patterns = [
        r'url\(["\']?([^"\')\s]+\.(woff2?|ttf|eot|otf))["\']?\)',
    ]
    for pattern in font_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if match:
                resources['fonts'].add(match)
    
    return resources

def remove_external_dependencies(html_content, location_key):
    """Remove or replace ALL external dependencies."""
    content = html_content
    
    # Remove Google Analytics and Tag Manager
    content = re.sub(r'<script[^>]*googletagmanager[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script[^>]*google-analytics[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script>\s*window\.dataLayer.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r"<script[^>]*gtag[^>]*>.*?</script>", '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove Facebook Pixel
    content = re.sub(r'<script[^>]*facebook[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove Stripe.js (not needed offline)
    content = re.sub(r'<script[^>]*stripe[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script[^>]+src=["\'][^"\']*stripe[^"\']*["\'][^>]*></script>', '', content, flags=re.IGNORECASE)
    
    # Remove Google Fonts - replace with comment
    content = re.sub(
        r'<link[^>]+href=["\'][^"\']*fonts\.googleapis\.com[^"\']*["\'][^>]*>',
        '<!-- Google Fonts removed for offline use -->',
        content,
        flags=re.IGNORECASE
    )
    
    # Remove external Font Awesome CDN - we'll use local if available
    content = re.sub(
        r'<link[^>]+href=["\'][^"\']*cdnjs\.cloudflare\.com[^"\']*font-awesome[^"\']*["\'][^>]*>',
        '<!-- Font Awesome CDN removed - using local version -->',
        content,
        flags=re.IGNORECASE
    )
    
    # Remove unpkg and other CDN scripts
    content = re.sub(
        r'<script[^>]+src=["\'][^"\']*unpkg\.com[^"\']*["\'][^>]*></script>',
        '<!-- CDN script removed for offline use -->',
        content,
        flags=re.IGNORECASE
    )
    
    # Replace form actions to prevent submission
    content = re.sub(
        r'<form([^>]*)action=["\'][^"\']*["\']',
        r'<form\1action="#" onsubmit="alert(\'Form submissions are not available offline. Please call the restaurant directly.\'); return false;"',
        content
    )
    
    # Add offline notice for external links (SpotHopper forms, ordering, etc.)
    external_services = [
        'tmt.spotapps.co',
        'spothopperapp.com',
        'waitrapp.com',
        'doordash.com',
        'ubereats.com',
        'grubhub.com',
    ]
    
    for service in external_services:
        content = re.sub(
            rf'href="([^"]*{re.escape(service)}[^"]*)"',
            r'href="#" onclick="alert(\'Online ordering and reservations are not available offline. Please call the restaurant directly.\'); return false;"',
            content
        )
    
    return content

def fix_internal_links(html_content, location_key):
    """Fix internal links to use local HTML files."""
    content = html_content
    
    # Fix links to other locations - use relative paths
    location_links = {
        'https://central.cafephoenicia.com': '../central/index.html',
        'https://zachary.cafephoenicia.com': '../zachary/index.html',
        'https://denhamsprings.cafephoenicia.com': '../denhamsprings/index.html',
        'http://central.cafephoenicia.com': '../central/index.html',
        'http://zachary.cafephoenicia.com': '../zachary/index.html',
        'http://denhamsprings.cafephoenicia.com': '../denhamsprings/index.html',
        '/central.cafephoenicia.com/': '../central/index.html',
        '/zachary.cafephoenicia.com/': '../zachary/index.html',
        '/denhamsprings.cafephoenicia.com/': '../denhamsprings/index.html',
    }
    
    for original, local in location_links.items():
        content = content.replace(f'href="{original}"', f'href="{local}"')
        content = content.replace(f"href='{original}'", f"href='{local}'")
    
    # Fix internal page links for each location
    page_links = {
        'central': {
            '/baton-rouge-central-cafe-phoenicia-central': 'index.html',
            '/central-cafe-phoenicia-central-food-menu': 'food-menu.html',
            '/baton-rouge-central-cafe-phoenicia-central-food-menu': 'food-menu.html',
            '/central-cafe-phoenicia-central-drink-menu': 'drink-menu.html',
            '/baton-rouge-central-cafe-phoenicia-central-drink-menu': 'drink-menu.html',
            '/central-cafe-phoenicia-central-happy-hours-specials': 'specials.html',
            '/baton-rouge-central-cafe-phoenicia-central-happy-hours-specials': 'specials.html',
            '/central-cafe-phoenicia-central-all-specials': 'specials.html',
            '/central-cafe-phoenicia-central-events': 'events.html',
            '/central-cafe-phoenicia-central-gift-cards': 'gift-cards.html',
            '/baton-rouge-central-cafe-phoenicia-central-gift-cards': 'gift-cards.html',
        },
        'denhamsprings': {
            '/denham-springs-cafe-phoenicia-denham-springs': 'index.html',
            '/denham-springs-cafe-phoenicia-denham-springs-food-menu': 'food-menu.html',
            '/denham-springs-cafe-phoenicia-denham-springs-drink-menu': 'drink-menu.html',
            '/denham-springs-cafe-phoenicia-denham-springs-happy-hours-specials': 'specials.html',
            '/denham-springs-cafe-phoenicia-denham-springs-all-specials': 'specials.html',
            '/denham-springs-cafe-phoenicia-denham-springs-events': 'events.html',
            '/denham-springs-cafe-phoenicia-denham-springs-gift-cards': 'gift-cards.html',
            '/denham-springs-cafe-phoenicia-denham-springs-catering-menu': 'catering-menu.html',
        },
        'zachary': {
            '/zachary-cafe-phoenicia-zachary': 'index.html',
            '/zachary-cafe-phoenicia-zachary-food-menu': 'food-menu.html',
            '/zachary-cafe-phoenicia-zachary-drink-menu': 'drink-menu.html',
            '/zachary-cafe-phoenicia-zachary-happy-hours-specials': 'specials.html',
            '/zachary-cafe-phoenicia-zachary-all-specials': 'specials.html',
            '/zachary-cafe-phoenicia-zachary-events': 'events.html',
            '/zachary-cafe-phoenicia-zachary-gift-cards': 'gift-cards.html',
        }
    }
    
    if location_key in page_links:
        for original, local in page_links[location_key].items():
            content = content.replace(f'href="{original}"', f'href="{local}"')
            content = content.replace(f"href='{original}'", f"href='{local}'")
    
    # Fix home links
    content = re.sub(r'href="/#"', 'href="index.html"', content)
    content = re.sub(r"href='/#'", "href='index.html'", content)
    content = re.sub(r'href="/"([^"])', r'href="index.html\1', content)
    
    return content

def replace_asset_urls(html_content, asset_map, location_key):
    """Replace ALL remote asset URLs with local paths."""
    content = html_content
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_assets = sorted(asset_map.items(), key=lambda x: len(x[0]), reverse=True)
    
    for remote_url, local_path in sorted_assets:
        # Adjust path for subdirectories
        adjusted_path = '../' + local_path
        
        # Replace in various contexts
        content = content.replace(f'"{remote_url}"', f'"{adjusted_path}"')
        content = content.replace(f"'{remote_url}'", f"'{adjusted_path}'")
        content = content.replace(f'({remote_url})', f'({adjusted_path})')
        content = content.replace(f'url({remote_url})', f'url({adjusted_path})')
        
        # Handle protocol-relative URLs
        if remote_url.startswith('http://'):
            protocol_relative = remote_url.replace('http://', '//')
            content = content.replace(f'"{protocol_relative}"', f'"{adjusted_path}"')
            content = content.replace(f"'{protocol_relative}'", f"'{adjusted_path}'")
        elif remote_url.startswith('https://'):
            protocol_relative = remote_url.replace('https://', '//')
            content = content.replace(f'"{protocol_relative}"', f'"{adjusted_path}"')
            content = content.replace(f"'{protocol_relative}'", f"'{adjusted_path}'")
    
    return content

def process_html_file(input_path, output_path, location_key):
    """Process a single HTML file to make it fully offline."""
    print(f"\n{'='*60}")
    print(f"Processing: {input_path.name}")
    print(f"{'='*60}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract ALL external resources
    resources = extract_all_external_resources(content)
    
    asset_map = {}
    
    # Download CSS files
    print(f"\n📄 CSS Files: {len(resources['css'])} found")
    for url in resources['css']:
        if url.startswith('http') or url.startswith('//'):
            local_path = download_asset(url, 'css')
            if local_path != url:
                asset_map[url] = local_path
    
    # Download JavaScript files
    print(f"\n📜 JavaScript Files: {len(resources['js'])} found")
    for url in resources['js']:
        if url.startswith('http') or url.startswith('//'):
            local_path = download_asset(url, 'js')
            if local_path != url:
                asset_map[url] = local_path
    
    # Download Images
    print(f"\n🖼️  Images: {len(resources['images'])} found")
    for url in resources['images']:
        if url.startswith('http') or url.startswith('//'):
            local_path = download_asset(url, 'images')
            if local_path != url:
                asset_map[url] = local_path
    
    # Download Videos
    print(f"\n🎥 Videos: {len(resources['videos'])} found")
    for url in resources['videos']:
        if url.startswith('http') or url.startswith('//'):
            local_path = download_asset(url, 'videos')
            if local_path != url:
                asset_map[url] = local_path
    
    # Download Fonts
    print(f"\n🔤 Fonts: {len(resources['fonts'])} found")
    for url in resources['fonts']:
        if url.startswith('http') or url.startswith('//'):
            local_path = download_asset(url, 'fonts', force_type='fonts')
            if local_path != url:
                asset_map[url] = local_path
    
    # Apply transformations
    print(f"\n🔧 Applying transformations...")
    content = remove_external_dependencies(content, location_key)
    content = fix_internal_links(content, location_key)
    content = replace_asset_urls(content, asset_map, location_key)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write processed file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Saved: {output_path}")

def create_main_index():
    """Create a main index page that links to all locations."""
    print(f"\n{'='*60}")
    print("Creating main landing page...")
    print(f"{'='*60}")
    
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cafe Phoenicia - Choose Your Location</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Georgia, 'Times New Roman', serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            text-align: center;
            color: #fff;
            max-width: 1200px;
            width: 100%;
        }
        
        .logo {
            max-width: 300px;
            margin: 0 auto 30px;
            display: block;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #d4af37;
            font-weight: normal;
        }
        
        h2 {
            font-size: 1.5em;
            margin-bottom: 50px;
            font-weight: normal;
            color: #ccc;
        }
        
        .locations {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .location-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 40px 30px;
            width: 300px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .location-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .location-card h3 {
            color: #d4af37;
            font-size: 1.8em;
            margin-bottom: 15px;
            font-weight: normal;
        }
        
        .location-card p {
            color: #ccc;
            margin-bottom: 25px;
            line-height: 1.6;
            font-size: 1.1em;
        }
        
        .visit-btn {
            display: inline-block;
            background: #d4af37;
            color: #1a1a2e;
            padding: 12px 35px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1em;
            transition: background 0.3s ease, transform 0.2s ease;
        }
        
        .visit-btn:hover {
            background: #f4cf67;
            color: #1a1a2e;
            text-decoration: none;
            transform: scale(1.05);
        }
        
        .offline-notice {
            margin-top: 40px;
            padding: 20px;
            background: rgba(255,193,7,0.2);
            border-radius: 10px;
            color: #ffc107;
            border: 1px solid rgba(255,193,7,0.3);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .offline-notice strong {
            font-size: 1.1em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            h2 {
                font-size: 1.2em;
            }
            
            .location-card {
                width: 100%;
                max-width: 350px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cafe Phoenicia</h1>
        <h2>Choose Your Location</h2>
        
        <div class="locations">
            <div class="location-card">
                <h3>Central</h3>
                <p>14319 Wax Rd<br>Baton Rouge, LA</p>
                <a href="central/index.html" class="visit-btn">Visit Site</a>
            </div>
            
            <div class="location-card">
                <h3>Zachary</h3>
                <p>5647 Main St<br>Zachary, LA</p>
                <a href="zachary/index.html" class="visit-btn">Visit Site</a>
            </div>
            
            <div class="location-card">
                <h3>Denham Springs</h3>
                <p>240 Range 12 Blvd Ste 111<br>Denham Springs, LA</p>
                <a href="denhamsprings/index.html" class="visit-btn">Visit Site</a>
            </div>
        </div>
        
        <div class="offline-notice">
            <strong>⚠️ Offline Mode</strong><br><br>
            This is an offline version of the Cafe Phoenicia website. 
            Online ordering, reservations, and form submissions are not available. 
            Please call the restaurant directly to place orders or make reservations.
        </div>
    </div>
</body>
</html>'''
    
    with open(SITE_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✅ Created index.html")

def main():
    """Main function to process all HTML files."""
    print("\n" + "="*60)
    print("🏗️  FULLY OFFLINE SITE BUILDER FOR CAFE PHOENICIA")
    print("="*60)
    print("\nThis will make the site completely self-contained")
    print("with NO external dependencies.\n")
    
    # Process each location
    for location_key, location_config in LOCATIONS.items():
        print(f"\n{'='*60}")
        print(f"📍 LOCATION: {location_key.upper()}")
        print(f"{'='*60}")
        
        source_dir = location_config['source_dir']
        output_dir = location_config['output_dir']
        
        if not source_dir.exists():
            print(f"⚠️  Warning: Source directory not found: {source_dir}")
            continue
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process all HTML files in source directory
        html_files = list(source_dir.glob('*.html'))
        print(f"\nFound {len(html_files)} HTML files to process")
        
        for html_file in html_files:
            # Determine output filename
            output_name = html_file.name.lower()
            
            # Map common filenames
            name_mappings = {
                'cafe phoenicia - central - central., baton rouge, la.html': 'index.html',
                'cafe phoenicia denham springs - denham springs, la.html': 'index.html',
                'cafe phoenicia - zachary - zachary , la.html': 'index.html',
                'cafe phoenicia - central - food menu.html': 'food-menu.html',
                'cafe phoenicia denham springs - food menu.html': 'food-menu.html',
                'cafe phoenicia - zachary - food menu.html': 'food-menu.html',
                'cafe phoenicia - central - drink menu.html': 'drink-menu.html',
                'cafe phoenicia denham springs - drink menu.html': 'drink-menu.html',
                'cafe phoenicia - zachary - drink menu.html': 'drink-menu.html',
                'cafe phoenicia - central - all specials.html': 'specials.html',
                'cafe phoenicia denham springs - all specials.html': 'specials.html',
                'cafe phoenicia - zachary - all specials.html': 'specials.html',
                'cafe phoenicia - central - gift cards.html': 'gift-cards.html',
                'cafe phoenicia denham springs - gift cards.html': 'gift-cards.html',
                'cafe phoenicia - zachary - gift cards.html': 'gift-cards.html',
                'cafe phoenicia denham springs - catering menu.html': 'catering-menu.html',
                'careers forum.html': 'careers.html',
                'careers.html': 'careers.html',
                'catering forum.html': 'catering.html',
                'catering page forum.html': 'catering.html',
                'catering page.html': 'catering.html',
                'group reservations and private parties.html': 'private-parties.html',
                'reservations forum.html': 'reservations.html',
            }
            
            output_name = name_mappings.get(output_name, output_name)
            output_path = output_dir / output_name
            
            process_html_file(html_file, output_path, location_key)
    
    # Create main index page
    create_main_index()
    
    print("\n" + "="*60)
    print("✅ PROCESSING COMPLETE!")
    print("="*60)
    print(f"\n📊 Total assets downloaded: {len(downloaded_assets)}")
    print("\n📁 Folder structure:")
    print("  Cafe-Phoenicia/")
    print("  ├── index.html (location selector)")
    print("  ├── assets/")
    print("  │   ├── css/")
    print("  │   ├── js/")
    print("  │   ├── images/")
    print("  │   ├── fonts/")
    print("  │   └── videos/")
    print("  ├── central/")
    print("  │   ├── index.html")
    print("  │   ├── food-menu.html")
    print("  │   ├── drink-menu.html")
    print("  │   └── ...")
    print("  ├── zachary/")
    print("  │   └── ...")
    print("  └── denhamsprings/")
    print("      └── ...")
    print("\n🌐 To test: Open index.html in a browser")
    print("   (Disable network to verify offline functionality)")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
