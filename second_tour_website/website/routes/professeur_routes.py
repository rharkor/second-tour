from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *

professeur_routes = Blueprint('professeur_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@professeur_routes.route('/')
@professeur_routes.route('/acceuil')
def acceuil():
    if main_security.test_session_connected(session, False):
        id_matieres = []
        for utilisateur in UTILISATEURS.query.all():
            if utilisateur.email == session['email']:
                for professeur in PROFESSEUR.query.all():
                    if professeur.id_utilisateur == utilisateur.id:
                        id_matieres.append(professeur.matiere)

        all_candidats = CANDIDATS.query.all()
        all_creneaux = CRENEAU.query.all()
        return render_template('professeur/acceuil.html', id_matieres=id_matieres, all_candidats=all_candidats, all_creneaux=all_creneaux)
    else:
        return redirect(url_for('main_routes.connexion'))

@professeur_routes.route('/deconnexion')
def deconnexion():
    if session['email']:
        session.pop('email', None)
    if session['password']:
        session.pop('password', None)
    flash('Vous avez correment été déconnecté', 'primary')
    return redirect(url_for('main_routes.index'))
