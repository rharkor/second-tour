from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..database.main_database import *
from ..function import main_security, main_sessions

main_routes = Blueprint('main_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@main_routes.route('/')
@main_routes.route('/index')
def index():
    return render_template('index.html')

@main_routes.route('/connexion', methods=['POST', 'GET'])
def connexion():
    if request.method == 'GET':
            if main_security.test_session_connected(session, True):
                return redirect(url_for('admin_routes.acceuil'))
            else:
                return render_template('connexion.html')
    else:
        form = request.form
        if not all([form['email'], form['password']]):
            flash('Une erreur est survenue', 'danger')
            return render_template('connexion.html')
        email, password = form['email'], form['password']
        # Verify that there valid
        try:
            user = UTILISATEURS.query.filter_by(email=email).first()
            # Verify that the user exist
            if user:
                # Verify the password
                if main_security.test_password(password, user):
                    # User exist
                    # Save in session
                    main_sessions.save_user(session, user)
                    # Go to dashboard
                    return redirect(url_for('admin_routes.acceuil'))
                else:
                    flash('Cet utilisateur n\'existe pas', 'warning')

        except Exception:
            flash('Cet utilisateur n\'existe pas', 'warning')
    return render_template('connexion.html')