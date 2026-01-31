#!/usr/bin/env python3
"""
Offline Site Builder for Cafe Phoenicia
This script processes downloaded HTML files and prepares them for offline hosting.
"""

import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
import ssl
import shutil

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
    'main': {
        'source_dir': SITE_DIR,
        'output_dir': SITE_DIR,
        'domain': 'cafephoenicia.com',
        'static_prefix': 'cafephoenicia--com'
    },
    'central': {
        'source_dir': SITE_DIR / 'central.cafephoenicia.com',
        'output_dir': SITE_DIR / 'central',
        'domain': 'central.cafephoenicia.com',
        'static_prefix': 'central--cafephoenicia--com'
    },
    'denhamsprings': {
        'source_dir': SITE_DIR / 'denhamsprings.cafephoenicia.com',
        'output_dir': SITE_DIR / 'denhamsprings',
        'domain': 'denhamsprings.cafephoenicia.com',
        'static_prefix': 'denhamsprings--cafephoenicia--com'
    },
    'zachary': {
        'source_dir': SITE_DIR / 'zachary.cafephoenicia.com',
        'output_dir': SITE_DIR / 'zachary',
        'domain': 'zachary.cafephoenicia.com',
        'static_prefix': 'zachary--cafephoenicia--com'
    }
}

# File mappings for each location
FILE_MAPPINGS = {
    'main': {
        "Cafe Phoenicia.html": "index.html",
    },
    'central': {
        "Cafe Phoenicia - Central - Central., Baton Rouge, LA.html": "index.html",
        "Cafe Phoenicia - Central - Food Menu.html": "food-menu.html",
        "Cafe Phoenicia - Central - Drink Menu.html": "drink-menu.html",
        "Cafe Phoenicia - Central - all specials.html": "specials.html",
        "Cafe Phoenicia - Central - Gift Cards.html": "gift-cards.html",
        "Careers forum.html": "careers.html",
        "Catering Forum.html": "catering.html",
        "Group Reservations and Private Parties.html": "private-parties.html",
    },
    'denhamsprings': {
        "Cafe Phoenicia Denham Springs - Denham Springs, LA.html": "index.html",
        "Cafe Phoenicia Denham Springs - Food Menu.html": "food-menu.html",
        "Cafe Phoenicia Denham Springs - Drink Menu.html": "drink-menu.html",
        "Cafe Phoenicia Denham Springs - all specials.html": "specials.html",
        "Cafe Phoenicia Denham Springs - Gift Cards.html": "gift-cards.html",
        "Cafe Phoenicia Denham Springs - Catering Menu.html": "catering-menu.html",
        "Careers Forum.html": "careers.html",
        "Catering Page Forum.html": "catering.html",
        "Group Reservations and Private Parties.html": "private-parties.html",
        "Reservations Forum.html": "reservations.html",
    },
    'zachary': {
        "Cafe Phoenicia - Zachary - Zachary , LA.html": "index.html",
        "Cafe Phoenicia - Zachary - Food Menu.html": "food-menu.html",
        "Cafe Phoenicia - Zachary - Drink Menu.html": "drink-menu.html",
        "Cafe Phoenicia - Zachary - all specials.html": "specials.html",
        "Cafe Phoenicia - Zachary - Gift Cards.html": "gift-cards.html",
        "Careers.html": "careers.html",
        "Catering Page.html": "catering.html",
        "Group Reservations and Private Parties.html": "private-parties.html",
    }
}

def get_safe_filename(url):
    """Convert URL to safe local filename."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    
    # Remove leading slash and replace remaining slashes
    filename = path.lstrip('/').replace('/', '_')
    
    # Handle query strings for cache-busted files
    if '?' in filename:
        filename = filename.split('?')[0]
    
    # Ensure we have an extension
    if not any(filename.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.ico']):
        if 'css' in url.lower():
            filename += '.css'
        elif 'js' in url.lower():
            filename += '.js'
    
    return filename

def download_asset(url, asset_type='images'):
    """Download an asset and return local path."""
    if url in downloaded_assets:
        return downloaded_assets[url]
    
    # Skip data URIs
    if url.startswith('data:'):
        return url
    
    # Skip external tracking/analytics
    skip_domains = ['googletagmanager.com', 'google-analytics.com', 'facebook.', 'googleapis.com/gtag']
    if any(domain in url for domain in skip_domains):
        return url
    
    # Determine target directory
    if asset_type == 'css' or '.css' in url:
        target_dir = CSS_DIR
        rel_path = 'assets/css'
    elif asset_type == 'js' or '.js' in url:
        target_dir = JS_DIR
        rel_path = 'assets/js'
    elif any(ext in url.lower() for ext in ['.woff', '.woff2', '.ttf', '.eot']):
        target_dir = FONTS_DIR
        rel_path = 'assets/fonts'
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
    
    downloaded_assets[url] = relative_path
    return relative_path

def extract_urls_from_html(html_content):
    """Extract all asset URLs from HTML content."""
    urls = {
        'css': set(),
        'js': set(),
        'images': set()
    }
    
    # CSS files
    css_patterns = [
        r'href=["\']([^"\']*\.css[^"\']*)["\']',
        r'href=["\']([^"\']+static\.spotapps\.co[^"\']+)["\']',
    ]
    for pattern in css_patterns:
        for match in re.findall(pattern, html_content):
            if 'spotapps.co' in match or match.startswith('css/'):
                urls['css'].add(match)
    
    # JS files
    js_patterns = [
        r'src=["\']([^"\']*\.js[^"\']*)["\']',
    ]
    for pattern in js_patterns:
        for match in re.findall(pattern, html_content):
            if 'spotapps.co' in match:
                urls['js'].add(match)
    
    # Images
    img_patterns = [
        r'src=["\']([^"\']+\.(png|jpg|jpeg|gif|webp|svg|ico)[^"\']*)["\']',
        r'url\(["\']?([^"\')\s]+\.(png|jpg|jpeg|gif|webp|svg))["\']?\)',
        r'data-src=["\']([^"\']+\.(png|jpg|jpeg|gif|webp|svg)[^"\']*)["\']',
        r'href=["\']([^"\']+\.(png|ico)[^"\']*)["\']',
    ]
    for pattern in img_patterns:
        for match in re.findall(pattern, html_content):
            if isinstance(match, tuple):
                match = match[0]
            if 'spotapps.co' in match:
                urls['images'].add(match)
    
    return urls

def fix_internal_links(html_content, location_key):
    """Fix internal links to use local HTML files."""
    content = html_content
    
    # Fix links to other locations
    location_links = {
        'https://central.cafephoenicia.com': 'central/index.html',
        'https://zachary.cafephoenicia.com': 'zachary/index.html',
        'https://denhamsprings.cafephoenicia.com': 'denhamsprings/index.html',
        'http://central.cafephoenicia.com': 'central/index.html',
        'http://zachary.cafephoenicia.com': 'zachary/index.html',
        'http://denhamsprings.cafephoenicia.com': 'denhamsprings/index.html',
    }
    
    for original, local in location_links.items():
        # Adjust path based on current location
        if location_key != 'main':
            local = '../' + local
        content = content.replace(f'href="{original}"', f'href="{local}"')
        content = content.replace(f"href='{original}'", f"href='{local}'")
    
    # Fix internal page links for each location
    page_links = {
        'central': {
            '/central-cafe-phoenicia-central-food-menu': 'food-menu.html',
            '/central-cafe-phoenicia-central-drink-menu': 'drink-menu.html',
            '/central-cafe-phoenicia-central-happy-hours-specials': 'specials.html',
            '/central-cafe-phoenicia-central-events': 'events.html',
            '/central-cafe-phoenicia-central-gift-cards': 'gift-cards.html',
        },
        'denhamsprings': {
            '/denham-springs-cafe-phoenicia-denham-springs-food-menu': 'food-menu.html',
            '/denham-springs-cafe-phoenicia-denham-springs-drink-menu': 'drink-menu.html',
            '/denham-springs-cafe-phoenicia-denham-springs-happy-hours-specials': 'specials.html',
            '/denham-springs-cafe-phoenicia-denham-springs-events': 'events.html',
            '/denham-springs-cafe-phoenicia-denham-springs-gift-cards': 'gift-cards.html',
            '/denham-springs-cafe-phoenicia-denham-springs-catering-menu': 'catering-menu.html',
        },
        'zachary': {
            '/zachary-cafe-phoenicia-zachary-food-menu': 'food-menu.html',
            '/zachary-cafe-phoenicia-zachary-drink-menu': 'drink-menu.html',
            '/zachary-cafe-phoenicia-zachary-happy-hours-specials': 'specials.html',
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
    content = re.sub(r'href="/"', 'href="index.html"', content)
    
    return content

def fix_asset_urls(html_content, asset_map, location_key):
    """Replace remote asset URLs with local paths."""
    content = html_content
    
    # Adjust path prefix based on location
    path_prefix = '../' if location_key != 'main' else ''
    
    for remote_url, local_path in asset_map.items():
        adjusted_path = path_prefix + local_path
        content = content.replace(remote_url, adjusted_path)
    
    return content

def disable_forms_and_tracking(html_content):
    """Disable form submissions and remove tracking for offline use."""
    content = html_content
    
    # Remove Google Tag Manager
    content = re.sub(r'<script[^>]*googletagmanager[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*window\.dataLayer.*?</script>', '', content, flags=re.DOTALL)
    
    # Remove gtag scripts
    content = re.sub(r"<script[^>]*gtag[^>]*>.*?</script>", '', content, flags=re.DOTALL)
    
    # Replace form actions to prevent submission
    content = re.sub(
        r'<form([^>]*)action=["\'][^"\']*["\']',
        r'<form\1action="#" onsubmit="alert(\'Form submissions are not available offline. Please call the restaurant directly.\'); return false;"',
        content
    )
    
    # Add offline notice for external links (SpotHopper forms)
    spothopper_links = [
        'tmt.spotapps.co/private-parties',
        'tmt.spotapps.co/catering',
        'tmt.spotapps.co/job-listings',
        'tmt.spotapps.co/reservations',
        'spothopperapp.com',
    ]
    
    for link in spothopper_links:
        content = re.sub(
            rf'href="([^"]*{re.escape(link)}[^"]*)"',
            r'href="#" onclick="alert(\'Online ordering and reservations are not available offline. Please call the restaurant directly.\'); return false;"',
            content
        )
    
    return content

def process_html_file(input_path, output_path, location_key):
    """Process a single HTML file."""
    print(f"\nProcessing: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract and download assets
    urls = extract_urls_from_html(content)
    
    asset_map = {}
    
    print(f"  Found {len(urls['css'])} CSS files")
    for url in urls['css']:
        local_path = download_asset(url, 'css')
        if local_path != url:
            asset_map[url] = local_path
    
    print(f"  Found {len(urls['js'])} JS files")
    for url in urls['js']:
        local_path = download_asset(url, 'js')
        if local_path != url:
            asset_map[url] = local_path
    
    print(f"  Found {len(urls['images'])} images")
    for url in urls['images']:
        local_path = download_asset(url, 'images')
        if local_path != url:
            asset_map[url] = local_path
    
    # Apply transformations
    content = fix_internal_links(content, location_key)
    content = fix_asset_urls(content, asset_map, location_key)
    content = disable_forms_and_tracking(content)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write processed file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  -> Saved: {output_path}")

def create_main_index():
    """Create a main index page that links to all locations."""
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cafe Phoenicia - Choose Your Location</title>
    <link rel="stylesheet" href="assets/css/web_cafephoenicia--com_lib_bootstrap_css_bootstrap.min.css">
    <style>
        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            text-align: center;
            color: #fff;
        }
        .logo {
            max-width: 300px;
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #d4af37;
        }
        h2 {
            font-size: 1.5em;
            margin-bottom: 40px;
            font-weight: normal;
            color: #ccc;
        }
        .locations {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 30px;
        }
        .location-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            width: 280px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .location-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .location-card h3 {
            color: #d4af37;
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        .location-card p {
            color: #ccc;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .visit-btn {
            display: inline-block;
            background: #d4af37;
            color: #1a1a2e;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s;
        }
        .visit-btn:hover {
            background: #f4cf67;
            color: #1a1a2e;
            text-decoration: none;
        }
        .offline-notice {
            margin-top: 40px;
            padding: 15px;
            background: rgba(255,193,7,0.2);
            border-radius: 10px;
            color: #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="assets/images/web_cafephoenicia--com_custom_logo.png" alt="Cafe Phoenicia Logo" class="logo">
        <h1>Cafe Phoenicia</h1>
        <h2>Choose Your Location</h2>
        
        <div class="locations">
            <div class="location-card">
                <h3>Central</h3>
                <p>14319 Wax Rd,<br>Baton Rouge, LA</p>
                <a href="central/index.html" class="visit-btn">Visit</a>
            </div>
            
            <div class="location-card">
                <h3>Zachary</h3>
                <p>5647 Main St,<br>Zachary, LA</p>
                <a href="zachary/index.html" class="visit-btn">Visit</a>
            </div>
            
            <div class="location-card">
                <h3>Denham Springs</h3>
                <p>240 Range 12 Blvd Ste 111,<br>Denham Springs, LA</p>
                <a href="denhamsprings/index.html" class="visit-btn">Visit</a>
            </div>
        </div>
        
        <div class="offline-notice">
            <strong>⚠️ Offline Mode:</strong> Online ordering and reservations are not available. 
            Please call the restaurant directly to place orders or make reservations.
        </div>
    </div>
</body>
</html>'''
    
    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(index_html)
    print("\nCreated main index.html")

def main():
    """Main function to process all HTML files."""
    print("=" * 60)
    print("Offline Site Builder for Cafe Phoenicia")
    print("=" * 60)
    
    # Process each location
    for location_key, location_config in LOCATIONS.items():
        print(f"\n{'='*60}")
        print(f"Processing location: {location_key.upper()}")
        print(f"{'='*60}")
        
        source_dir = location_config['source_dir']
        output_dir = location_config['output_dir']
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get file mapping for this location
        file_mapping = FILE_MAPPINGS.get(location_key, {})
        
        for original_name, target_name in file_mapping.items():
            input_path = source_dir / original_name
            output_path = output_dir / target_name
            
            if input_path.exists():
                process_html_file(input_path, output_path, location_key)
            else:
                print(f"Warning: {original_name} not found in {source_dir}")
    
    # Create main index page
    create_main_index()
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print(f"Total assets downloaded: {len(downloaded_assets)}")
    print("=" * 60)
    print("\nFolder structure:")
    print("  cafephoenicia.com/")
    print("  ├── index.html (location selector)")
    print("  ├── assets/")
    print("  │   ├── css/")
    print("  │   ├── js/")
    print("  │   └── images/")
    print("  ├── central/")
    print("  │   ├── index.html")
    print("  │   ├── food-menu.html")
    print("  │   └── ...")
    print("  ├── zachary/")
    print("  │   └── ...")
    print("  └── denhamsprings/")
    print("      └── ...")
    print("\nTo test: Open index.html in a browser")

if __name__ == "__main__":
    main()
