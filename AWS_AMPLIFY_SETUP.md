# AWS Amplify Deployment Guide for Cafe Phoenicia

This guide will help you deploy the Cafe Phoenicia offline website to AWS Amplify.

## 📋 Prerequisites

- AWS Account
- Git repository (GitHub, GitLab, Bitbucket, or AWS CodeCommit)
- Source HTML files in the repository

## 🚀 Quick Start

### Option 1: Deploy via AWS Amplify Console (Recommended)

1. **Push to Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Cafe Phoenicia offline site"
   git branch -M main
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

2. **Connect to AWS Amplify**
   - Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
   - Click "New app" → "Host web app"
   - Select your Git provider (GitHub, GitLab, Bitbucket, etc.)
   - Authorize AWS Amplify to access your repository
   - Select the repository and branch (main)

3. **Configure Build Settings**
   - Amplify will auto-detect the `amplify.yml` file
   - Review the build settings (should match the amplify.yml configuration)
   - Click "Next"

4. **Review and Deploy**
   - Review all settings
   - Click "Save and deploy"
   - Wait for the build to complete (5-10 minutes)

5. **Access Your Site**
   - Once deployed, you'll get a URL like: `https://main.d1234567890.amplifyapp.com`
   - You can add a custom domain later

### Option 2: Deploy via AWS CLI

1. **Install Amplify CLI**
   ```bash
   npm install -g @aws-amplify/cli
   amplify configure
   ```

2. **Initialize Amplify**
   ```bash
   amplify init
   ```
   - Enter project name: `cafe-phoenicia`
   - Enter environment name: `production`
   - Choose default editor: (your choice)
   - Choose app type: `javascript`
   - Framework: `none`
   - Source directory: `.`
   - Distribution directory: `.`
   - Build command: `python3 build_fully_offline.py`
   - Start command: (leave empty)

3. **Add Hosting**
   ```bash
   amplify add hosting
   ```
   - Select: `Hosting with Amplify Console`
   - Choose: `Manual deployment`

4. **Publish**
   ```bash
   amplify publish
   ```

## 📁 Configuration Files

The following files have been created for AWS Amplify:

### `amplify.yml`
Main build configuration for AWS Amplify. Defines:
- Python 3.9 runtime
- Build commands
- Output artifacts

### `buildspec.yml`
Alternative build specification (for AWS CodeBuild if needed)

### `package.json`
Node.js package configuration with build scripts

### `requirements.txt`
Python dependencies (none required - uses standard library only)

### `.gitignore`
Excludes unnecessary files from Git repository

## 🔧 Build Process

When you deploy to Amplify, it will:

1. **Install Phase**: Set up Python 3.9 environment
2. **Pre-Build Phase**: Verify Python installation
3. **Build Phase**: Run `build_fully_offline.py` to:
   - Process all HTML files from source directories
   - Download external assets (CSS, JS, images, fonts)
   - Convert URLs to local paths
   - Remove tracking and analytics
   - Create offline-ready pages
4. **Deploy Phase**: Upload all files to Amplify hosting

## 🌐 Custom Domain Setup

After deployment, you can add a custom domain:

1. Go to your Amplify app
2. Click "Domain management" in the left sidebar
3. Click "Add domain"
4. Enter your domain (e.g., `cafephoenicia.com`)
5. Follow the DNS configuration instructions
6. Wait for SSL certificate provisioning (5-10 minutes)

### Subdomain Configuration

You can set up subdomains for each location:
- `central.cafephoenicia.com` → `/central/index.html`
- `zachary.cafephoenicia.com` → `/zachary/index.html`
- `denhamsprings.cafephoenicia.com` → `/denhamsprings/index.html`

Add redirects in Amplify Console:
1. Go to "Rewrites and redirects"
2. Add custom rules:
   ```
   Source: https://central.cafephoenicia.com
   Target: /central/index.html
   Type: 200 (Rewrite)
   
   Source: https://zachary.cafephoenicia.com
   Target: /zachary/index.html
   Type: 200 (Rewrite)
   
   Source: https://denhamsprings.cafephoenicia.com
   Target: /denhamsprings/index.html
   Type: 200 (Rewrite)
   ```

## 🔒 Security & Performance

### HTTPS
- Amplify automatically provisions SSL certificates
- All traffic is encrypted via HTTPS

### CDN
- Amplify uses Amazon CloudFront CDN
- Global edge locations for fast loading
- Automatic caching

### Performance Optimizations
- Enable compression in Amplify settings
- Images are already optimized
- Minified CSS and JS

## 💰 Pricing

AWS Amplify Hosting pricing (as of 2026):
- **Build minutes**: $0.01 per build minute
- **Hosting**: $0.15 per GB stored per month
- **Data transfer**: $0.15 per GB served
- **Free tier**: 1000 build minutes/month, 15 GB served/month

**Estimated monthly cost for this site**:
- Storage: ~50MB = $0.01/month
- Builds: ~5 minutes/build × 10 builds = $0.50/month
- Data transfer: ~100 GB = $15/month (if heavily used)

**Total**: ~$15-20/month (depending on traffic)

## 🔄 Continuous Deployment

Once connected to Git, Amplify will automatically:
- Build and deploy on every push to main branch
- Create preview deployments for pull requests
- Notify you of build status via email

### Manual Deployment

To manually trigger a deployment:
1. Go to your Amplify app
2. Click "Run build" on the main branch
3. Wait for build to complete

## 📊 Monitoring

AWS Amplify provides:
- **Build logs**: View detailed build output
- **Access logs**: Monitor traffic and errors
- **Metrics**: Page views, data transfer, etc.
- **Alarms**: Set up CloudWatch alarms

## 🐛 Troubleshooting

### Build Fails

**Problem**: Python script fails during build

**Solution**: Check build logs in Amplify Console
- Ensure source HTML files are in the repository
- Verify `build_fully_offline.py` has correct paths
- Check Python version (should be 3.9+)

### Assets Not Loading

**Problem**: Images or CSS not loading after deployment

**Solution**: 
- Check file paths are relative (not absolute)
- Verify all assets are in the `assets/` directory
- Clear browser cache and reload

### Slow Build Times

**Problem**: Build takes longer than 10 minutes

**Solution**:
- Most assets should already be downloaded
- Consider pre-processing source files
- Use Amplify's build cache

## 📝 Environment Variables

If needed, you can add environment variables in Amplify Console:
1. Go to "Environment variables"
2. Add key-value pairs
3. Access in build script via `os.environ['VARIABLE_NAME']`

## 🔗 Useful Links

- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [Amplify Console](https://console.aws.amazon.com/amplify/)
- [Amplify Pricing](https://aws.amazon.com/amplify/pricing/)
- [Custom Domain Setup](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html)

## ✅ Deployment Checklist

Before deploying:
- [ ] Source HTML files are in repository
- [ ] `build_fully_offline.py` script is tested locally
- [ ] All configuration files are committed
- [ ] `.gitignore` excludes unnecessary files
- [ ] Git repository is pushed to remote
- [ ] AWS account is set up
- [ ] Domain name is ready (if using custom domain)

After deploying:
- [ ] Site loads correctly at Amplify URL
- [ ] All three locations are accessible
- [ ] Images and styles load properly
- [ ] Navigation works between locations
- [ ] Test on mobile devices
- [ ] Set up custom domain (if desired)
- [ ] Configure monitoring and alerts

## 🎉 Success!

Once deployed, your Cafe Phoenicia website will be:
- ✅ Globally available via CDN
- ✅ Automatically HTTPS secured
- ✅ Fast loading worldwide
- ✅ Automatically backed up
- ✅ Easy to update (just push to Git)

---

**Need Help?** Contact AWS Support or refer to the [Amplify documentation](https://docs.aws.amazon.com/amplify/).
