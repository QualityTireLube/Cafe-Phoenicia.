#!/bin/bash
# Test script to verify the site has no external dependencies

echo "=========================================="
echo "OFFLINE DEPENDENCY CHECK"
echo "=========================================="
echo ""

# Check for external URLs in HTML files
echo "🔍 Checking for external dependencies..."
echo ""

# Google Fonts
echo "1. Google Fonts:"
count=$(grep -r "fonts.googleapis.com" central/ zachary/ denhamsprings/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No Google Fonts references found"
else
    echo "   ⚠️  Found $count Google Fonts references"
    grep -r "fonts.googleapis.com" central/ zachary/ denhamsprings/ 2>/dev/null | head -3
fi
echo ""

# CDN Links
echo "2. CDN Links (cdnjs, unpkg, etc.):"
count=$(grep -rE "(cdnjs\.cloudflare\.com|unpkg\.com|cdn\.jsdelivr\.net)" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No CDN references found (or all commented out)"
else
    echo "   ⚠️  Found $count CDN references"
    grep -rE "(cdnjs\.cloudflare\.com|unpkg\.com|cdn\.jsdelivr\.net)" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | head -3
fi
echo ""

# External JavaScript
echo "3. External JavaScript:"
count=$(grep -rE "src=['\"]https?://" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No external JavaScript found (or all commented out)"
else
    echo "   ⚠️  Found $count external JavaScript references"
    grep -rE "src=['\"]https?://" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | head -3
fi
echo ""

# External CSS
echo "4. External CSS:"
count=$(grep -rE "href=['\"]https?://.*\.css" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No external CSS found (or all commented out)"
else
    echo "   ⚠️  Found $count external CSS references"
    grep -rE "href=['\"]https?://.*\.css" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | head -3
fi
echo ""

# Cloudinary Images
echo "5. Cloudinary Images:"
count=$(grep -r "cloudinary.com" central/ zachary/ denhamsprings/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No Cloudinary references found"
else
    echo "   ⚠️  Found $count Cloudinary references"
    grep -r "cloudinary.com" central/ zachary/ denhamsprings/ 2>/dev/null | head -3
fi
echo ""

# Protocol-relative URLs (//example.com)
echo "6. Protocol-relative URLs:"
count=$(grep -rE "(src|href)=['\"]//[a-zA-Z]" central/ zachary/ denhamsprings/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$count" -eq "0" ]; then
    echo "   ✅ No protocol-relative URLs found"
else
    echo "   ⚠️  Found $count protocol-relative URLs"
    grep -rE "(src|href)=['\"]//[a-zA-Z]" central/ zachary/ denhamsprings/ 2>/dev/null | head -3
fi
echo ""

echo "=========================================="
echo "ASSET CHECK"
echo "=========================================="
echo ""

# Count local assets
css_count=$(find assets/css -type f 2>/dev/null | wc -l | tr -d ' ')
js_count=$(find assets/js -type f 2>/dev/null | wc -l | tr -d ' ')
img_count=$(find assets/images -type f 2>/dev/null | wc -l | tr -d ' ')
font_count=$(find assets/fonts -type f 2>/dev/null | wc -l | tr -d ' ')

echo "📦 Local Assets:"
echo "   CSS files:    $css_count"
echo "   JS files:     $js_count"
echo "   Images:       $img_count"
echo "   Fonts:        $font_count"
echo ""

echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo ""

# Calculate total issues
total_issues=$(grep -rE "(fonts\.googleapis\.com|cdnjs\.cloudflare\.com|unpkg\.com|src=['\"]https?://|href=['\"]https?://.*\.css|cloudinary\.com|(src|href)=['\"]//[a-zA-Z])" central/ zachary/ denhamsprings/ 2>/dev/null | grep -v "<!-- " | wc -l | tr -d ' ')

if [ "$total_issues" -eq "0" ]; then
    echo "✅ SUCCESS: Site appears to be fully offline-capable!"
    echo "   No external dependencies detected."
    echo ""
    echo "🌐 To test:"
    echo "   1. Open index.html in a web browser"
    echo "   2. Disable network (airplane mode or disconnect WiFi)"
    echo "   3. Navigate through the site"
    echo ""
else
    echo "⚠️  ATTENTION: Found $total_issues potential external dependencies"
    echo "   Review the items above and re-run build_fully_offline.py if needed"
    echo ""
fi

echo "=========================================="
