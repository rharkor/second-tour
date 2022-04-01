import logging
import traceback
from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from flask.helpers import flash
import os


from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *
from ..main_website import app

register_routes = Blueprint('register_routes', __name__,
                            template_folder='templates',
                            static_folder='static')


@register_routes.route('/', methods=['POST', 'GET'])
def register():
    
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
            "name": "website-professeur:website-professeur-compte",
            "data": {
                "target": "website-professeur:website-professeur-compte"
            }
        })
    
    if request.method == "POST":
        form = request.form
        if 'email' in form and 'token' in form and 'password' in form:
            try:
                response = ask_api("data/fetchfilter/token", {"token": form['token']})
                if response.status_code != 200:
                    flash("Une erreur est survenue lors de la récupération des données", "danger")
                exist = response.json()[0] if response else None
                # exist = TOKEN.query.filter_by(token=form['token']).one()
                if exist and exist['email'] == form['email']:
                    user = main_database.add_account(form['email'], form['password'], 'Professeur', output=True)
                    if user[1][1] == 'danger':
                        flash(user[1][0], user[1][1])
                    else:
                        logging.warning(f"Le compte du professeur {form['email']} à bien été crée")
                        main_database.delete_token(form['token'])
                        logging.warning(f"Le token à en conséquent été supprimé")
                        return redirect(url_for('main_routes.connexion'))
                else:
                    flash("L'adresse saisie est incorrecte", "danger")
            except Exception:
                traceback.print_exc()
                flash("L'adresse saisie est incorrecte", "danger")
        return render_template('register/register.html', token=form["token"], email=form["email"])
    else:
        token = request.args.get('token')
        try:
            response = ask_api("data/fetchfilter/token", {"token": token})
            if response.status_code != 200:
                flash("Une erreur est survenue lors de la récupération des données", "danger")
            if response:
                email = response.json()[0]['email'] if response.json() else None
            else:
                email = None
            # email = TOKEN.query.filter_by(token=token).one().email
            return render_template('register/register.html', token=token, email=email)
        except Exception:
            traceback.print_exc()
            logging.warning("Invalid token")
            return render_template('register/register.html', token="error", email="error")
