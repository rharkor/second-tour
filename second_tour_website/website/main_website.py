from flask import Flask, render_template, request, redirect, flash, session, url_for
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

# Import sql classes
from .database.main_database import UTILISATEURS

# Configure the routes blueprint
from .routes.main_routes import main_routes
app.register_blueprint(main_routes, url_prefix='/')


def run(debug_mode=False):
    # Run the database
    db.create_all()

    # Run the website
    app.run(debug=debug_mode)