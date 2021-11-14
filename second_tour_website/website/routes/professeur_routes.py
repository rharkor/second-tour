import logging
from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *

professeur_routes = Blueprint('professeur_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@professeur_routes.route('/')
@professeur_routes.route('/accueil')
def accueil():
    if main_security.test_session_connected(session, False):
        id_matieres = []
        all_professeurs = []
        professeurs = PROFESSEUR.query.all()
        for professeur in professeurs:
            all_professeurs.append(professeur.as_dict())
        id_salle = []
        for utilisateur in UTILISATEURS.query.all():
            if utilisateur.email == session['email']:
                for professeur in PROFESSEUR.query.all():
                    if professeur.id_utilisateur == utilisateur.id:
                        id_matieres.append(professeur.matiere)
                        id_salle.append(professeur.salle)
        salles = SALLE.query.all()
        all_salles = []
        for salle in salles:
            all_salles.append(salle.as_dict())
        all_candidats = CANDIDATS.query.all()
        all_creneaux = CRENEAU.query.all()
        return render_template('professeur/accueil.html', id_matieres=id_matieres, all_candidats=all_candidats, all_creneaux=all_creneaux, id_salle=id_salle, all_professeurs=all_professeurs, all_salles=all_salles)
    else:
        return redirect(url_for('main_routes.connexion'))

@professeur_routes.route('/deconnexion')
def deconnexion():
    if session['email']:
        session.pop('email', None)
    if session['password']:
        session.pop('password', None)
    flash('Vous avez correment été déconnecté', 'primary')
    logging.warning('Vous avez correctement été déconnecté')
    return redirect(url_for('main_routes.index'))
