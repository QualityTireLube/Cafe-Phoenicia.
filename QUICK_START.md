# Quick Start Guide - Cafe Phoenicia AWS Amplify Deployment

## 🚀 Deploy in 5 Minutes

### Prerequisites
- [ ] AWS Account
- [ ] Git installed
- [ ] GitHub/GitLab/Bitbucket account

### Step 1: Run Deploy Script (2 minutes)
```bash
./deploy-to-amplify.sh
```
Follow the prompts to:
- Initialize Git
- Add remote repository
- Commit changes
- Push to Git

### Step 2: Connect AWS Amplify (2 minutes)
1. Open [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
2. Click **"New app"** → **"Host web app"**
3. Select your Git provider
4. Authorize and select repository
5. Choose **main** branch

### Step 3: Deploy (1 minute)
1. Amplify auto-detects `amplify.yml` ✅
2. Review settings
3. Click **"Save and deploy"**
4. Wait ~5-10 minutes ⏱️

### Step 4: Done! 🎉
Your site is live at: `https://main.d1234567890.amplifyapp.com`

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `amplify.yml` | AWS Amplify build config |
| `build_fully_offline.py` | Builds offline site |
| `deploy-to-amplify.sh` | Deployment helper |
| `AWS_AMPLIFY_SETUP.md` | Full instructions |

---

## 🔧 Common Commands

### Test Locally
```bash
python3 build_fully_offline.py
open index.html
```

### Deploy Updates
```bash
git add .
git commit -m "Update menu"
git push
```
*Amplify auto-deploys!*

### Test Offline
```bash
./test_offline.sh
```

---

## 💰 Pricing
~$15-20/month for typical traffic
- Storage: $0.01/month
- Builds: $0.50/month
- Data: $15/month (100GB)

---

## 🌐 Add Custom Domain

1. In Amplify Console → **"Domain management"**
2. Click **"Add domain"**
3. Enter: `cafephoenicia.com`
4. Follow DNS instructions
5. Wait ~10 minutes for SSL

---

## 📞 Support

- **Full Guide**: `AWS_AMPLIFY_SETUP.md`
- **Deployment Info**: `DEPLOYMENT_SUMMARY.md`
- **AWS Docs**: https://docs.aws.amazon.com/amplify/

---

## ✅ Checklist

- [ ] Run `./deploy-to-amplify.sh`
- [ ] Push to Git repository
- [ ] Connect to AWS Amplify
- [ ] Deploy and wait
- [ ] Test live site
- [ ] Add custom domain (optional)

---

**That's it! Your site is live! 🎉**
