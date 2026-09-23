# Quick Start - Deploy Your Backend

Your code is ready! Follow these steps:

## Step 1: Create GitHub Repository (2 min)

1. Go to https://github.com/new
2. Repository name: `portfolio-contact-form-backend`
3. **Make it PUBLIC**
4. Click "Create repository"
5. Copy the HTTPS URL (looks like `https://github.com/YOUR-USERNAME/portfolio-contact-form-backend.git`)

## Step 2: Push Code to GitHub (1 min)

Replace `YOUR-USERNAME` with your GitHub username and run:

```bash
cd ~/113hw#4
git remote add origin https://github.com/YOUR-USERNAME/portfolio-contact-form-backend.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render (5 min)

1. Go to https://render.com
2. Sign up with GitHub (easier!)
3. Click "New" → "Web Service"
4. Select "Connect a repository" → choose your backend repo
5. Fill in:
   - **Name**: `portfolio-contact-form`
   - **Environment**: Python 3
   - **Region**: Any (I pick US)
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

6. Scroll down, click "Advanced" → "Add Environment Variable" (3 times):

   **Variable 1:**
   - Key: `SUPABASE_URL`
   - Value: `<your Project URL>`

   **Variable 2:**
   - Key: `SUPABASE_KEY`
   - Value: `<your sb_secret_... key from Supabase Settings → API Keys>`

   **Variable 3:**
   - Key: `ADMIN_KEY`
   - Value: `<same ADMIN_KEY as your .env>`

7. Click "Create Web Service"
8. Wait 2-3 minutes for deployment to finish
9. Render shows your public URL (e.g., `https://portfolio-contact-form.onrender.com`)
10. **Copy this URL** - you need it next

## Step 4: Update Frontend URL (1 min)

1. Open `/Users/rohitkottomtharayil/rkottomt.github.io/contact-form.html`
2. Find line 229: `const BACKEND_URL = 'https://portfolio-contact.onrender.com';`
3. Replace with your actual Render URL (from Step 3.9)
4. Save and commit:

```bash
cd ~/rkottomt.github.io
git add contact-form.html
git commit -m "Update backend URL to deployed Render service"
git push
```

## Step 5: Test It Works! (2 min)

1. Go to https://rkottomt.github.io/contact-form.html
2. Fill out the form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Message: "Testing my deployed backend!"
3. Click "Send Message"
4. You should see "Message Sent!" ✓
5. Check Supabase dashboard → Table Editor → `questions` table
6. Your submission should appear! ✓

## Step 6: Record Video (5 min)

Show:
1. Filling out form on your portfolio
2. Success message appearing
3. Going to Supabase dashboard to show it was saved
4. (Optional) Show another submission to prove it works twice

## Step 7: Submit Assignment

Create the GitHub repo (from Step 1) link and video link and submit!

---

## Troubleshooting

**"Failed to deploy" on Render**
- Check your environment variables are exactly correct
- Make sure `SUPABASE_KEY` is the secret key (starts with `sb_secret_`)

**Form shows "Connection failed"**
- Wait 30 seconds (Render free tier wakes up from sleep)
- Check that BACKEND_URL in contact-form.html exactly matches your Render URL
- Check browser console (F12 → Console tab) for error

**Submissions not saving**
- Go to your Render service → Logs tab
- Look for error messages
- Verify `questions` table exists in Supabase (Table Editor)

**Can't push to GitHub**
- Check you ran: `git remote add origin https://github.com/YOUR-USERNAME/portfolio-contact-form-backend.git`
- Make sure you're in the right directory: `cd ~/113hw#4`
- Verify you have GitHub SSH key set up or use HTTPS with personal access token

---

**You're almost done!** Once deployed, you have a real backend service handling form submissions. Perfect for the assignment. 🎉
