from flask import Flask, render_template, request, flash, redirect, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import datetime
from .security import main_security


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "HEby4gbqFGFtSCeV"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=3)

# Create the database
db = SQLAlchemy(app)
from .database.main_data import *


@app.route('/')
@app.route('/index')
def index():
    if 'email' in session and 'password' in session:
        email = session['email']
        password = session['password']
        # Test the connection
        user = UTILISATEURS.query.filter_by(email=email).first()
        if user and password == user.password:
            flash(f'Connected with : {email}', 'success')
    return render_template('index.html')

@app.route('/hello/<phrase>')
def hello(phrase):
    return phrase

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = request.form
        user = UTILISATEURS.query.filter_by(email=form['email']).first()
        if user:
            if main_security.test_password(password=form['password'], user=user):
                session['email'] = form['email']
                session['password'] = user.password
                session.permanent = True
                return redirect(url_for('index'))
        flash('Le mot de passe ou l\'adresse mail ne sont pas valides', 'danger')
        return render_template('login.html')

# ONLY FOR DEBUG ELSE DEACTIVE IT
@app.route('/register')
def register():
    email = "louis@huort.com"
    password = "Test123"
    hashed_password = main_security.hash_password(password)
    user = UTILISATEURS(email, hashed_password, True)
    try:
        db.session.add(user)
        db.session.commit()
        flash('L\'utilisateur à bien été crée', 'success')
        session['email'] = email
        session['password'] = password
        session.permanent = True
    except sqlalchemy.exc.IntegrityError:
        flash('Cet utilisateur existe déjà', 'danger')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', default=None)
    session.pop('password', default=None)
    return redirect(url_for('index'))


def run():
    # Create database
    run_db()
    # Run website
    app.run(debug=True)

def run_db():
    db.create_all()

