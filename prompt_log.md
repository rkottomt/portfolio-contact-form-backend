# Prompt Log - Portfolio Contact Form Backend

## AI Tools Used
- **Claude Sonnet 5** - Main AI model for architecture, code generation, and planning
- **Claude Haiku 4.5** - Used for refinements and quick iterations

## Key Implementation Prompts

### Prompt 1: Backend Architecture (No API Costs)
"Build a Flask backend for a portfolio contact form that:
- Accepts form submissions with name, email, and question
- Stores submissions in Supabase PostgreSQL database (free tier)
- Validates email format and message length on backend
- Has a /submit-question endpoint for frontend to call
- Includes a /questions admin endpoint to view submissions
- Uses CORS for GitHub Pages frontend
- Has no API costs using only free tier services"

Result: Created `app.py` with Supabase integration and validation.

### Prompt 2: Database Schema
"Design a simple PostgreSQL table for storing contact form submissions:
- Auto-incrementing ID
- Name, email, and question fields
- Timestamp for when submitted
- Indexed for efficient querying"

Result: SQL schema in README for creating the `questions` table.

### Prompt 3: Frontend Form Component
"Create an HTML/CSS/JavaScript contact form that:
- Validates input before sending to backend
- Shows loading state during submission
- Displays success/error messages
- Counts characters in the message field
- Matches the existing portfolio style
- Works on desktop and mobile"

Result: Created `contact-form.html` with full form validation and UX.

### Prompt 4: Security & Validation
"Implement backend validation for contact form:
- Email format validation using regex
- Required field checking
- Message length limits (5-2000 chars)
- Admin key authentication for viewing submissions
- Input sanitization"

Result: Validation functions in `app.py` protecting against malformed input.

## Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Hosting**: Render (backend), GitHub Pages (frontend)
- **Python Client**: supabase==2.0.1

## Form Validation Details

**Client-side (browser):**
- All fields required
- Email format check
- Message length: 5-2000 characters
- Real-time character counter

**Server-side (backend):**
- Name not empty
- Email format: regex validation
- Question length: 5-2000 characters
- Returns descriptive error messages

## Database Schema

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

## Testing Prompts Used

1. "Send me a test message" - Test basic functionality
2. "Invalid email test" - Test email validation (should fail)
3. "Short msg" - Test minimum length validation (should fail)
4. "This is a valid message about a project inquiry" - Test success case
5. Very long 2000+ character message - Test maximum length (should fail)

## Supabase Setup

Free tier includes:
- Unlimited database rows
- 500 MB storage
- 2 GB monthly bandwidth
- Perfect for storing form submissions

No configuration needed beyond creating the table and getting API credentials.

## Deployment Considerations

- Environment variables stored on Render (not in code)
- Supabase credentials never exposed in frontend
- Admin key kept secret for viewing submissions
- Rate limiting handled by email (implicit - users submit once)
- All connections use HTTPS

## Future Enhancements

- Email notifications when new submissions arrive
- Admin dashboard UI to manage submissions
- Spam filtering/reCAPTCHA integration
- Response email template
- Export submissions as CSV
