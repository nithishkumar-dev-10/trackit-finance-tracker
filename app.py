import os
from flask import Flask

from home import home_bp
from users import users_bp
from income import income_bp
from expense import expense_bp
from summary import summary_bp
from profile.routes import profile_bp
from db.db import init_db

app = Flask(__name__)

# Secret key from environment variable (IMPORTANT for production)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")

# Initialize database tables
init_db()

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(users_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(summary_bp)
app.register_blueprint(profile_bp)