# Portfolio Contact Form Backend

A Flask backend service that handles form submissions from your portfolio website and stores them in a Supabase database. Visitors can ask questions or send feedback, which you can view on a dashboard.

## Features

- **Form Validation** — Validates email, name, and question fields on backend
- **Supabase Database** — Stores submissions in a fully managed PostgreSQL database (free tier)
- **Admin Dashboard** — View all submissions with timestamps
- **CORS Enabled** — Works with frontend hosted on GitHub Pages
- **No API Costs** — Uses free Supabase tier

## API Endpoints

### POST /submit-question
Submits a contact form question.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "question": "I'd like to learn more about your projects..."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Question submitted successfully! Thank you for reaching out.",
  "id": 123
}
```

**Error Response (400):**
```json
{
  "error": "Invalid email format"
}
```

### GET /questions
Retrieve all submitted questions (requires admin key).

**Headers:**
```
X-Admin-Key: your-admin-secret-key
```

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "question": "How did you build your portfolio?",
      "created_at": "2026-09-23T15:30:00.000Z"
    }
  ],
  "count": 1
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

## Setup & Installation

### 1. Create Supabase Account & Database

1. Go to https://supabase.com and sign up (free)
2. Create a new project
3. Go to SQL Editor and run this to create the table:

```sql
CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  question TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index for faster queries
CREATE INDEX idx_questions_created_at ON questions(created_at DESC);
```

4. Get your credentials:
   - Go to Settings → API
   - Copy your `Project URL` (SUPABASE_URL)
   - Copy your `anon public` key (SUPABASE_KEY)

### 2. Local Development

```bash
cd ~/113hw#4
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
ADMIN_KEY=your-secret-admin-key-here
```

Run the server:
```bash
python app.py
```

Server runs at `http://127.0.0.1:5000`

### 3. Test Locally

```bash
curl -X POST http://127.0.0.1:5000/submit-question \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "question": "How did you build this?"
  }'
```

Test the health endpoint:
```bash
curl http://127.0.0.1:5000/health
```

## Deployment to Render

1. Create GitHub repository (public):
```bash
cd ~/113hw#4
git init
git add .
git commit -m "Initial commit: Portfolio contact form backend"
git remote add origin https://github.com/YOUR-USERNAME/portfolio-contact-backend.git
git push -u origin main
```

2. Create Render Web Service:
   - Go to https://render.com
   - Connect your GitHub repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`

3. Add Environment Variables in Render dashboard:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key
   - `ADMIN_KEY`: A secret key for admin access (make it random/long)

4. Deploy and get your public URL (e.g., `https://portfolio-contact.onrender.com`)

## Frontend Integration

Your portfolio's contact form will call:
```javascript
fetch('https://portfolio-contact.onrender.com/submit-question', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: formName,
    email: formEmail,
    question: formQuestion
  })
})
```

See `contact-form.html` in your portfolio repo for implementation.

## Viewing Submissions

You have two ways to view submissions:

### Option 1: Supabase Dashboard (Easiest)
1. Go to your Supabase project
2. Click "Table Editor"
3. Select the `questions` table
4. View all submissions with timestamps

### Option 2: Admin API Endpoint
```bash
curl http://localhost:5000/questions \
  -H "X-Admin-Key: your-admin-key"
```

## Security & Privacy

- **Email Validation** — Backend validates email format before storing
- **Input Validation** — Question must be 5-2000 characters
- **Admin Key** — Only authorized users can view submissions
- **CORS** — Configured to work with GitHub Pages frontend
- **No Secrets in Frontend** — Admin key stays on backend only
- **Supabase Security** — Your data is encrypted at rest

## Supabase Free Tier Limits

- **Storage**: 500 MB per project
- **Bandwidth**: 2 GB per month
- **Database rows**: Unlimited
- **Realtime**: 2 concurrent connections

For this assignment, you'll easily stay within free tier limits (each form submission is ~500 bytes).

## Troubleshooting

### "SUPABASE_URL and SUPABASE_KEY required"
- Make sure `.env` file exists locally and has correct values
- On Render, check that environment variables are set in the dashboard

### Questions not saving
1. Check backend logs (Render → Logs tab)
2. Verify Supabase credentials are correct
3. Make sure `questions` table exists in Supabase
4. Check browser console for error messages from frontend

### "Invalid email format" error
- Frontend is sending an improperly formatted email
- Backend validates with regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

## Architecture

- **Backend**: Flask on Render (serverless)
- **Database**: Supabase PostgreSQL (managed)
- **Frontend**: HTML/CSS/JS on GitHub Pages
- **Communication**: HTTPS + CORS
- **Deployment**: Automatic from GitHub (Render auto-deploys on git push)

## Next Steps

1. ✅ Create Supabase account and database
2. ✅ Test backend locally
3. ✅ Deploy to Render
4. ✅ Create contact form on portfolio
5. ✅ Test end-to-end
6. ✅ Record demo video
7. ✅ Submit assignment
