import logging
import traceback
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
    # ask for data
    response = ask_api("data/fetchmulti", ["candidat", "creneau", "serie", "matiere", "salle"])
    if response.status_code != 200:
        flash("Une erreur est survenue lors de la récupération des données", "danger")
    all_candidats, all_creneaux, all_series, all_matieres, all_salles = response.json()
    
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
            logging.warning('Une erreur est survenue, il m\anquai l\'email ou le mot de passe')
            return render_template('connexion.html')
        email, password = form['email'], form['password']
        # Verify that there valid
        try:
            response = ask_api("data/fetchfilter/utilisateur", {"email": email, "admin": "true"})
            if response.status_code != 200:
                flash("Une erreur est survenue lors de la récupération des données", "danger")
                logging.warning("Une erreur est survenue lors de la recuperation des donnees utilisateur")
            user = response.json()[0] if response.json() else None
            # user = UTILISATEUR.query.filter_by(email=email, admin=True).first()
            if not user:
                response = ask_api("data/fetchfilter/utilisateur", {"email": email, "admin": "false"})
                if response.status_code != 200:
                    flash("Une erreur est survenue lors de la récupération des données", "danger")
                    logging.warning("Une erreur est survenue lors de la recuperation des donnees utilisateur")
                user = response.json()[0] if response.json() else None
                # user = UTILISATEUR.query.filter_by(email=email, admin=False).first()
            # Verify that the user exist
            if user:
                # Verify the password
                if main_security.test_password(password, user):
                    # User exist
                    # Save in session
                    main_sessions.save_user(session, user)
                    # Go to dashboard
                    logging.warning('Connexion reussie')
                    return redirect(url_for('admin_routes.accueil'))
                else:
                    flash('Cet utilisateur n\'existe pas', 'warning')
                    logging.warning('Cet utilisateur n\'existe pas (incorrect password)')
                    return render_template('connexion.html'), 401
            else:
                flash('Cet utilisateur n\'existe pas', 'warning')
                logging.warning('Cet utilisateur n\'existe pas')
                return render_template('connexion.html'), 401
            
        except Exception:
            flash('Cet utilisateur n\'existe pas', 'warning')
            logging.warning(traceback.format_exc().encode("utf-8"))
            logging.warning('Cet utilisateur n\'existe pas + erreur code')
    return render_template('connexion.html')

@main_routes.route('/cgu')
def cgu():
    return render_template('cgu.html')
