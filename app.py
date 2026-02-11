from flask import Flask,render_template
from home import home_bp
from users import users_bp
from income import income_bp
from expense import expense_bp
from summary import summary_bp
from profile.routes import profile_bp
from db.db import init_db
app=Flask(__name__)
init_db()
app.secret_key = "super-secret-key"
app.register_blueprint(home_bp)
app.register_blueprint(users_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(summary_bp)
app.register_blueprint(profile_bp)