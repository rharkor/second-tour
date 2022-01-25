import logging
import traceback
from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from flask.helpers import flash
from itsdangerous import exc

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *
from ..main_website import app

register_routes = Blueprint('register_routes', __name__,
                            template_folder='templates',
                            static_folder='static')


@register_routes.route('/', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        form = request.form
        if 'email' in form and 'token' in form and 'password' in form:
            try:
                exist = TOKEN.query.filter_by(token=form['token']).one()
                if exist:
                    user = main_database.add_account(form['email'], form['password'], 'Professeur', output=True, id_prof=1)
                    if user[1][1] == 'danger':
                        flash(user[1][0], user[1][1])
                    else:
                        logging.warning(f"Le compte du professeur {form['email']} à bien été crée")
                        main_database.delete_token(form['token'])
                        logging.warning(f"Le token à en conséuqent été supprimé")
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
            email = TOKEN.query.filter_by(token=token).one().email
            return render_template('register/register.html', token=token, email=email)
        except Exception:
            traceback.print_exc()
            return render_template('register/register.html', token="error", email="error")
