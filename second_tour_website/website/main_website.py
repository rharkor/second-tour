from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# Global website
app = Flask(__name__)


# Configure the website
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "HEby4gbqFGFtSCeV"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)

db = SQLAlchemy(app)

# Configure the routes blueprint
from .routes.main_routes import main_routes
from .routes.admin_routes import admin_routes
app.register_blueprint(main_routes, url_prefix='/')
app.register_blueprint(admin_routes, url_prefix='/admin')


def run(debug_mode=False):
    # Run the database
    db.create_all()

    # Run the website
    app.run(debug=debug_mode)