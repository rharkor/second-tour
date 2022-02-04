import logging
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
    all_candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
    all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
    all_series = SERIE.query.all()
    all_matieres = MATIERES.query.all()
    all_salles = SALLE.query.all()
    
    return render_template('index.html', all_candidats=all_candidats, all_creneaux=all_creneaux, all_series=all_series, all_matieres=all_matieres, all_salles=all_salles)

@main_routes.route('/connexion', methods=['POST', 'GET'])
def connexion():
    if request.method == 'GET':
            if main_security.test_session_connected(session, True):
                return redirect(url_for('admin_routes.accueil'))
            elif main_security.test_session_connected(session, False):
                return redirect(url_for('professeur_routes.accueil'))
            else:
                return render_template('connexion.html')
    else:
        form = request.form
        if 'email' not in form or 'password' not in form:
            flash('Une erreur est survenue', 'danger')
            logging.warning('Une erreur est survenue, il m\anquais l\'email ou le mot de passe')
            return render_template('connexion.html')
        email, password = form['email'], form['password']
        # Verify that there valid
        try:
            user = UTILISATEURS.query.filter_by(email=email, admin=True).first()
            if not user:
                user = UTILISATEURS.query.filter_by(email=email, admin=False).first()
            # Verify that the user exist
            if user:
                # Verify the password
                if main_security.test_password(password, user):
                    # User exist
                    # Save in session
                    main_sessions.save_user(session, user)
                    # Go to dashboard
                    logging.warning('Connexion réussie')
                    return redirect(url_for('admin_routes.accueil'))
                else:
                    flash('Cet utilisateur n\'existe pas', 'warning')
                    logging.warning('Cet utilisateur n\'existe pas')
            else:
                flash('Cet utilisateur n\'existe pas', 'warning')
                logging.warning('Cet utilisateur n\'existe pas')
            
        except Exception:
            flash('Cet utilisateur n\'existe pas', 'warning')
            logging.warning('Cet utilisateur n\'existe pas')
    return render_template('connexion.html')