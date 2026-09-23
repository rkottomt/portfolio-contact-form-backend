from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('SUPABASE_URL and SUPABASE_KEY environment variables are required')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@app.route('/submit-question', methods=['POST'])
def submit_question():
    """Submit a question/contact form."""
    try:
        data = request.json

        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        question = data.get('question', '').strip()

        if not name or not email or not question:
            return jsonify({'error': 'Name, email, and question are required'}), 400

        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if len(question) < 5:
            return jsonify({'error': 'Question must be at least 5 characters'}), 400

        if len(question) > 2000:
            return jsonify({'error': 'Question must be less than 2000 characters'}), 400

        # Insert into Supabase
        response = supabase.table('questions').insert({
            'name': name,
            'email': email,
            'question': question,
            'created_at': datetime.utcnow().isoformat()
        }).execute()

        return jsonify({
            'success': True,
            'message': 'Question submitted successfully! Thank you for reaching out.',
            'id': response.data[0]['id'] if response.data else None
        }), 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Failed to submit question. Please try again.'}), 500


@app.route('/questions', methods=['GET'])
def get_questions():
    """Retrieve all questions (admin endpoint)."""
    try:
        # Simple auth check - requires API key
        api_key = request.headers.get('X-Admin-Key')
        admin_key = os.getenv('ADMIN_KEY')

        if not admin_key or api_key != admin_key:
            return jsonify({'error': 'Unauthorized'}), 401

        response = supabase.table('questions').select('*').order('created_at', desc=True).execute()

        return jsonify({
            'questions': response.data,
            'count': len(response.data)
        }), 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Failed to retrieve questions'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        # Test Supabase connection
        supabase.table('questions').select('count', count='exact').execute()
        return jsonify({'status': 'ok', 'database': 'connected'}), 200
    except:
        return jsonify({'status': 'ok', 'database': 'disconnected'}), 200


if __name__ == '__main__':
    app.run(debug=True)
