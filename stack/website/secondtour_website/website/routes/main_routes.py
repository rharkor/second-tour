import logging
import traceback
from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash
import requests


from ..database.main_database import *
from ..function import main_security, main_sessions

main_routes = Blueprint('main_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@main_routes.route('/')
@main_routes.route('/index')
def index():
    
    if(os.getenv("NETWORK_VISU") == "true"):
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website:website-home",
            "data": {
                "target": "website:website-home"
            }
        })
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website-home:website-home-home",
            "data": {
                "target": "website-home:website-home-home"
            }
        })
    
    # ask for data
    response = ask_api("data/fetchmulti", ["candidat", "creneau", "serie", "matiere", "salle"])
    if response.status_code != 200:
        flash("Une erreur est survenue lors de la récupération des données", "danger")
    all_candidats, all_creneaux, all_series, all_matieres, all_salles = response.json()
    
    all_creneaux.sort(key=lambda creneau: creneau['debut_preparation'])
    for creneau in all_creneaux:
                creneau["debut_preparation"] = datetime.strptime(creneau["debut_preparation"], '%a %b %d %H:%M:%S %Y') if type(creneau["debut_preparation"]) == str else creneau["debut_preparation"]
                creneau["fin_preparation"] = datetime.strptime(creneau["fin_preparation"], '%a %b %d %H:%M:%S %Y') if type(creneau["fin_preparation"]) == str else creneau["fin_preparation"]
                creneau["fin"] = datetime.strptime(creneau["fin"], '%a %b %d %H:%M:%S %Y') if type(creneau["fin"]) == str else creneau["fin"]

    return render_template('index.html', all_candidats=all_candidats, all_creneaux=all_creneaux, all_series=all_series, all_matieres=all_matieres, all_salles=all_salles)

@main_routes.route('/connexion', methods=['POST', 'GET'])
def connexion():
    
    if(os.getenv("NETWORK_VISU") == "true"):
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website:website-home",
            "data": {
                "target": "website:website-home"
            }
        })
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website-home:website-home-connexion",
            "data": {
                "target": "website-home:website-home-connexion"
            }
        })
    
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
    if(os.getenv("NETWORK_VISU") == "true"):
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website:website-home",
            "data": {
                "target": "website:website-home"
            }
        })
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website-home:website-home-cgu",
            "data": {
                "target": "website-home:website-home-cgu"
            }
        })
    
    return render_template('cgu.html')


if(os.getenv("NETWORK_VISU") == "true"):
    
    
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-home",
        "data": {
                "name": "Accueil",
                "id": "website-home",
                "size": 46,
                "fsize": 30
        },
        "position": {
            "x": 353,
            "y": 707
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website:website-home",
        "data": {
                "id": "website:website-home",
                "weight": 1,
                "source": "website",
                "target": "website-home"
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-home-home",
        "data": {
                "name": "Pade d'accueil",
                "id": "website-home-home",
                "size": 28,
                "fsize": 20
        },
        "position": {
            "x": 272,
            "y": 745
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website-home:website-home-home",
        "data": {
                "id": "website-home:website-home-home",
                "weight": 1,
                "source": "website-home",
                "target": "website-home-home"
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-home-cgu",
        "data": {
                "name": "CGU",
                "id": "website-home-cgu",
                "size": 28,
                "fsize": 20
        },
        "position": {
            "x": 315,
            "y": 782
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website-home:website-home-cgu",
        "data": {
                "id": "website-home:website-home-cgu",
                "weight": 1,
                "source": "website-home",
                "target": "website-home-cgu"
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "node",
        "name": "website-home-connexion",
        "data": {
                "name": "Connexion",
                "id": "website-home-connexion",
                "size": 28,
                "fsize": 20
        },
        "position": {
            "x": 372,
            "y": 793
        }
    })
    requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
        "type": "edge",
        "name": "website-home:website-home-connexion",
        "data": {
                "id": "website-home:website-home-connexion",
                "weight": 1,
                "source": "website-home",
                "target": "website-home-connexion"
        }
    })