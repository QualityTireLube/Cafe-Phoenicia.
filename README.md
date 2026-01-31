# Cafe Phoenicia - Offline Website

This is a fully offline-capable version of the Cafe Phoenicia website for all three locations: Central, Zachary, and Denham Springs.

## 🌟 Features

- **100% Offline Capable**: All CSS, JavaScript, images, and fonts are stored locally
- **No External Dependencies**: Works without internet connection
- **Three Locations**: Central, Zachary, and Denham Springs
- **Full Menu Access**: View food and drink menus for each location
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📁 Structure

```
Cafe-Phoenicia/
├── index.html              # Main landing page (location selector)
├── assets/                 # All local assets
│   ├── css/               # 187 CSS files
│   ├── js/                # 95 JavaScript files
│   ├── images/            # 128 images
│   ├── fonts/             # 3 font files
│   └── videos/            # Video files
├── central/               # Central location pages
│   ├── index.html
│   ├── food-menu.html
│   ├── drink-menu.html
│   ├── specials.html
│   ├── gift-cards.html
│   ├── careers.html
│   ├── catering.html
│   └── private-parties.html
├── zachary/               # Zachary location pages
│   └── (similar structure)
└── denhamsprings/         # Denham Springs location pages
    └── (similar structure)
```

## 🚀 Usage

### Viewing the Site Locally

1. **Open in Browser**: Simply double-click `index.html` or open it in any web browser
2. **Select Location**: Choose Central, Zachary, or Denham Springs
3. **Browse**: Navigate through menus, specials, and other pages

### Testing Offline

1. Open `index.html` in your browser
2. Enable airplane mode or disconnect from WiFi
3. Navigate through the site - everything should work!

### Deploying to AWS Amplify

This site is ready to deploy to AWS Amplify for global hosting with CDN:

1. **Quick Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```
   Then connect your repository in the [AWS Amplify Console](https://console.aws.amazon.com/amplify/)

2. **Detailed Instructions**: See [AWS_AMPLIFY_SETUP.md](AWS_AMPLIFY_SETUP.md) for complete deployment guide

**Benefits of AWS Amplify**:
- ✅ Global CDN with fast loading worldwide
- ✅ Automatic HTTPS/SSL certificates
- ✅ Continuous deployment from Git
- ✅ Custom domain support
- ✅ ~$15-20/month for typical traffic

## 🛠️ Building from Source

If you need to rebuild the offline site from the original downloaded HTML files:

```bash
python3 build_fully_offline.py
```

This script will:
- Download all external CSS, JavaScript, images, and fonts
- Convert all URLs to local paths
- Remove external tracking and analytics
- Disable online forms and ordering
- Create a clean, offline-ready version

## 📝 Notes

### What Works Offline
- ✅ All menus (food and drinks)
- ✅ Specials and events pages
- ✅ Gift cards information
- ✅ Gallery images
- ✅ Location information
- ✅ Navigation between locations

### What Doesn't Work Offline
- ❌ Online ordering (Waitr, DoorDash, etc.)
- ❌ Reservations and private party bookings
- ❌ Job applications
- ❌ Form submissions
- ❌ Google Maps integration

All disabled features show an alert directing users to call the restaurant directly.

## 📞 Contact Information

### Central Location
- **Address**: 14319 Wax Rd, Baton Rouge, LA
- **Phone**: (225) 302-5443

### Zachary Location
- **Address**: 5647 Main St, Zachary, LA
- **Phone**: (225) 654-4455

### Denham Springs Location
- **Address**: 240 Range 12 Blvd Ste 111, Denham Springs, LA
- **Phone**: (225) 664-7900

## 🔧 Technical Details

### Dependencies Removed
- Google Fonts (replaced with system fonts)
- Google Analytics & Tag Manager
- Facebook Pixel
- Stripe.js
- External CDNs (cdnjs, unpkg, etc.)
- Cloudinary image hosting

### Assets Downloaded
- **CSS**: 187 files including Bootstrap, Font Awesome, custom styles
- **JavaScript**: 95 files including jQuery, plugins, and custom scripts
- **Images**: 128 files including photos, logos, and graphics
- **Fonts**: 3 Font Awesome font files

### Browser Compatibility
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 📦 Deployment Files

The following files are included for AWS Amplify deployment:

- `amplify.yml` - AWS Amplify build configuration
- `buildspec.yml` - Alternative build specification
- `package.json` - Node.js package configuration
- `requirements.txt` - Python dependencies (none required)
- `.gitignore` - Git exclusions
- `AWS_AMPLIFY_SETUP.md` - Complete deployment guide

## 📄 License

This offline version is for internal use only. All content and images are property of Cafe Phoenicia.

## 🆘 Troubleshooting

### Images Not Loading
- Ensure all files in the `assets/` folder are present
- Check browser console for any missing file errors

### Styles Not Applied
- Make sure CSS files in `assets/css/` are intact
- Clear browser cache and reload

### JavaScript Errors
- Check that all JS files in `assets/js/` are present
- Open browser developer tools to see specific errors

## 📅 Last Updated

January 31, 2026

---

**Note**: This is an offline version. For online ordering, reservations, or current information, please visit the live website or call the restaurant directly.
