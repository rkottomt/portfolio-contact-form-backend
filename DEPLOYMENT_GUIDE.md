# Deployment Guide - Portfolio Contact Form Backend

## Overview

This backend stores contact form submissions from your portfolio in a **free Supabase database**. No API costs!

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Account
1. Go to https://supabase.com
2. Sign up with GitHub or email (free tier)
3. Create a new project (choose any region)
4. Wait for the project to initialize (~1-2 minutes)

### 1.2 Create Questions Table
1. Go to the SQL Editor in your project
2. Create a new query and paste:

```sql
CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  question TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_created_at ON questions(created_at DESC);
```

3. Click "Run" to create the table

### 1.3 Get Your Credentials
1. Click "Settings" (bottom left)
2. Click "API"
3. Copy these values:
   - **Project URL** → This is your `SUPABASE_URL`
   - **anon public** key → This is your `SUPABASE_KEY`

Save these somewhere safe - you'll need them next.

## Step 2: Test Locally

### 2.1 Set Up Python Environment
```bash
cd ~/113hw#4
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.3 Create .env File
Create a file named `.env` in the project root with:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
ADMIN_KEY=your-secret-admin-key-make-this-random
```

**Important**: Never commit this file to Git! It's in `.gitignore`.

### 2.4 Run Backend Locally
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 2.5 Test the Endpoint
Open another terminal and run:

```bash
curl -X POST http://127.0.0.1:5000/submit-question \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "question": "This is a test message"
  }'
```

You should get back:
```json
{
  "success": true,
  "message": "Question submitted successfully! Thank you for reaching out.",
  "id": 1
}
```

Check your Supabase dashboard - the submission should appear in the `questions` table!

### 2.6 Test the Admin Endpoint
```bash
curl http://127.0.0.1:5000/questions \
  -H "X-Admin-Key: your-secret-admin-key-make-this-random"
```

Should return all your submissions.

### 2.7 Test Frontend Locally

1. Edit `contact-form.html` and change line 229:
   ```javascript
   const BACKEND_URL = 'http://127.0.0.1:5000';
   ```

2. Open `contact-form.html` in your browser

3. Fill out the form and submit

4. You should see a success message and the submission appears in Supabase

5. When done testing, change the URL back to the Render URL

## Step 3: Deploy to Render

### 3.1 Create GitHub Repository
```bash
cd ~/113hw#4
git init
git add .
git commit -m "Initial commit: Portfolio contact form backend"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/portfolio-contact-backend.git
git push -u origin main
```

Make sure the repo is **public**.

### 3.2 Deploy on Render

1. Go to https://render.com
2. Sign up (use GitHub account for easier setup)
3. Click "New" → "Web Service"
4. Select "Connect a repository"
5. Choose your GitHub repo
6. Fill in the form:
   - **Name**: `portfolio-contact-form` (or similar)
   - **Environment**: Python 3
   - **Region**: Choose closest to you
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (for this assignment)

7. Click "Advanced" to add environment variables

### 3.3 Add Environment Variables on Render
Click "Add Environment Variable" three times:

1. First variable:
   - Key: `SUPABASE_URL`
   - Value: (paste your Supabase URL)

2. Second variable:
   - Key: `SUPABASE_KEY`
   - Value: (paste your Supabase anon key)

3. Third variable:
   - Key: `ADMIN_KEY`
   - Value: (make up a random long string, e.g., `sk-admin-abc123xyz789`)

8. Click "Create Web Service"

Render will deploy automatically. Wait 2-3 minutes for it to finish. You'll see your public URL like:
```
https://portfolio-contact-form.onrender.com
```

### 3.4 Test Deployed Backend

```bash
curl -X POST https://portfolio-contact-form.onrender.com/submit-question \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "question": "Testing deployed backend"
  }'
```

### 3.5 Update Frontend with Deployed URL

In `contact-form.html`, change line 229:
```javascript
const BACKEND_URL = 'https://portfolio-contact-form.onrender.com';
```

Push to your portfolio repo:
```bash
cd ~/rkottomt.github.io
git add contact-form.html
git commit -m "Update contact form backend URL to deployed service"
git push
```

### 3.6 Test End-to-End

1. Go to https://rkottomt.github.io/contact-form.html
2. Fill out the form and submit
3. You should see a success message
4. Check your Supabase dashboard to confirm it was saved

## Step 4: View Submissions

You have two ways to check submissions:

### Option 1: Supabase Dashboard (Recommended)
1. Go to your Supabase project
2. Click "Table Editor" (left sidebar)
3. Select the `questions` table
4. See all submissions with names, emails, and timestamps

### Option 2: API Endpoint
```bash
curl https://portfolio-contact-form.onrender.com/questions \
  -H "X-Admin-Key: your-admin-key"
```

## Troubleshooting

### "SUPABASE_URL and SUPABASE_KEY required"
- Check your Render environment variables are set correctly
- Look in Render dashboard Settings → Environment
- Make sure values are copied exactly (no extra spaces)

### Form submissions not saving
1. Check Render logs: Click on your service → Logs
2. Verify Supabase table exists: Go to Supabase → Table Editor
3. Check browser console: F12 → Console tab in your browser
4. Verify backend URL in contact-form.html is correct

### "Unauthorized" when viewing admin endpoint
- Make sure you're sending the correct `X-Admin-Key` header
- Make sure the admin key matches what you set in Render environment variables

### Slow response time
- Render free tier services sleep after 15 minutes of inactivity
- First request wakes the service (takes 10-30 seconds)
- Subsequent requests are fast
- This is fine for the assignment!

## Important Security Notes

✅ **API keys are stored on backend only** (Render environment variables)
✅ **No secrets in frontend code or GitHub**
✅ **.gitignore prevents .env from being committed**
✅ **All connections use HTTPS**
✅ **Supabase data is encrypted**
✅ **Admin key protects viewing submissions**

## Supabase Free Tier Limits

- **Rows**: Unlimited ✓
- **Storage**: 500 MB per project ✓
- **Bandwidth**: 2 GB per month ✓
- **For this project**: You'll use <1 MB (plenty!)

## Next Steps

1. ✅ Create Supabase account and table
2. ✅ Test locally
3. ✅ Deploy to Render
4. ✅ Update frontend with Render URL
5. ✅ Test end-to-end
6. Record a demo video showing:
   - Filling out the contact form
   - Success message appearing
   - Checking submissions in Supabase dashboard
7. Submit assignment with links to repos and video

## Free Resources Used

- ✅ Supabase (free PostgreSQL database)
- ✅ Render (free backend hosting)
- ✅ GitHub Pages (free frontend hosting)
- ✅ GitHub (free code repository)

**Total cost: $0** 🎉
