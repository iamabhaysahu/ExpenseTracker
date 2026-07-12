from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "security_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from Expensetracker.routes.signin import signin_bp
    from Expensetracker.routes.login  import login_bp
    from Expensetracker.routes.profile import profile_bp

    app.register_blueprint(signin_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(profile_bp)


    return app