# app.py
# Main Flask application entry point for Estate X
# Run with: python app.py

import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp

# Load environment variables from .env file if present
load_dotenv()

# ── App Configuration ──────────────────────────────────────────────────────────

app = Flask(__name__)

# Secret key for sessions and flash messages (change this in production)
app.secret_key = os.getenv('SECRET_KEY', 'estate_x_secret_key_2024')

# Maximum upload size: 5 MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Ensure uploads directory exists at startup
os.makedirs('uploads', exist_ok=True)

# ── Register Blueprints ────────────────────────────────────────────────────────

app.register_blueprint(auth_bp)    # /register, /login, /logout
app.register_blueprint(admin_bp)   # /admin/...
app.register_blueprint(user_bp)    # /, /properties, /property/<id>, etc.


# ── Serve Uploaded Property Images ────────────────────────────────────────────

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve files from the uploads directory."""
    return send_from_directory('uploads', filename)


# ── Run the App ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # debug=True enables auto-reload on code changes (disable in production)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_ENV') != 'production', host='0.0.0.0', port=port)

