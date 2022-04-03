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
    if(os.getenv("NETWORK_VISU") == "true"):
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website:website-professeur",
            "data": {
                "target": "website:website-professeur"
            }
        })
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website-professeur:website-professeur-accueil",
            "data": {
                "target": "website-professeur:website-professeur-accueil"
            }
        })
    
    
    if main_security.test_session_connected(session, False):
        id_matieres = []
        all_professeurs = []
        response_prof = ask_api(
            "data/fetch/professeur", {})
        professeurs = response_prof.json()
        for professeur in professeurs:
            all_professeurs.append(professeur)
        id_salle = []
        response_utilisateurs = ask_api(
            "data/fetch/utilisateur", {})
        for utilisateur in response_utilisateurs.json():
            if utilisateur['email'] == session['email']:
                response_prof = ask_api(
                    "data/fetch/professeur", {})
                for professeur in response_prof.json():
                    if professeur['id_professeur'] == utilisateur['id_professeur']:
                        response_liste = ask_api(
                            "data/fetch/liste_matiere", {})
                        for liste_matiere in response_liste.json():
                            if liste_matiere['id_professeur'] == professeur['id_professeur']:
                                id_matieres.append(liste_matiere['id_matiere'])
                        id_salle.append(professeur['salle'])
        response_salle = ask_api(
            "data/fetch/salle", {})
        salles = response_salle.json()
        all_salles = []
        for salle in salles:
            all_salles.append(salle)
        response_candidat = ask_api(
            "data/fetch/candidat", {})
        all_candidats = response_candidat.json()
        response_creneau = ask_api(
            "data/fetch/creneau", {})
        all_creneaux = response_creneau.json()
        for creneau in all_creneaux:
            creneau["debut_preparation"] = datetime.strptime(creneau["debut_preparation"], '%a %b %d %H:%M:%S %Y') if type(
                creneau["debut_preparation"]) == str else creneau["debut_preparation"]
            creneau["fin_preparation"] = datetime.strptime(creneau["fin_preparation"], '%a %b %d %H:%M:%S %Y') if type(
                creneau["fin_preparation"]) == str else creneau["fin_preparation"]
            creneau["fin"] = datetime.strptime(creneau["fin"], '%a %b %d %H:%M:%S %Y') if type(
                creneau["fin"]) == str else creneau["fin"]
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


if(os.getenv("NETWORK_VISU") == "true"):
    
    
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-professeur",
        "data": {
                "name": "Professeur",
                "id": "website-professeur",
                "size": 46,
                "fsize": 30
        },
        "position": {
            "x": 711,
            "y": 615
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website:website-professeur",
        "data": {
                "id": "website:website-professeur",
                "weight": 1,
                "source": "website",
                "target": "website-professeur"
        }
    })
    
    
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-professeur-accueil",
        "data": {
                "name": "Accueil",
                "id": "website-professeur-accueil",
                "size": 28,
                "fsize": 20
        },
        "position": {
            "x": 825,
            "y": 670
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website-professeur:website-professeur-accueil",
        "data": {
                "id": "website-professeur:website-professeur-accueil",
                "weight": 1,
                "source": "website-professeur",
                "target": "website-professeur-accueil"
        }
    })
    
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-professeur-compte",
        "data": {
                "name": "Création de compte",
                "id": "website-professeur-compte",
                "size": 28,
                "fsize": 20
        },
        "position": {
            "x": 825,
            "y": 611
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website-professeur:website-professeur-compte",
        "data": {
                "id": "website-professeur:website-professeur-compte",
                "weight": 1,
                "source": "website-professeur",
                "target": "website-professeur-compte"
        }
    })
