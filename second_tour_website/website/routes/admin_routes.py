from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security, main_sessions, main_database
from ..database.main_database import *

admin_routes = Blueprint('admin_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@admin_routes.route('/')
@admin_routes.route('/acceuil')
def acceuil():
    if main_security.test_session_connected(session, True):
        return render_template('admin/acceuil.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/candidats')
def candidats():
    if main_security.test_session_connected(session, True):
        return render_template('admin/candidats.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/salles')
def salles():
    if main_security.test_session_connected(session, True):
        return render_template('admin/salles.html')
    else:
        return redirect(url_for('main_routes.connexion'))
 
@admin_routes.route('/professeurs')
def professeurs():
    if main_security.test_session_connected(session, True):
        return render_template('admin/professeurs.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/series', methods=['POST', 'GET'])
def series():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'serie' in form and 'specialite1' in form:
                    result = main_database.add_serie(form['serie'], form['specialite1'], form['specialite2'] if 'specialite2' in form else None)
                    flash(result[0], result[1])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_serie(form['id']):
                        flash(r[0], r[1])
                
        all_series = SERIE.query.all()
        return render_template('admin/series.html', all_series=all_series)
    else:
        return redirect(url_for('main_routes.connexion'))
        
@admin_routes.route('/matieres')
def matieres():
    if main_security.test_session_connected(session, True):
        return render_template('admin/matieres.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/comptes', methods=['POST', 'GET'])
def comptes():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'email' in form and 'password' in form and 'type' in form:
                    result = main_database.add_account(form['email'], form['password'], form['type'])
                    flash(result[0], result[1])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_account(form['id']):
                        flash(r[0], r[1])
        all_users = UTILISATEURS.query.all()
        return render_template('admin/comptes.html', all_users=all_users)
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/deconnexion')
def deconnexion():
    if session['email']:
        session.pop('email', None)
    if session['password']:
        session.pop('password', None)
    flash('Vous avez correment été déconnecté', 'primary')
    return redirect(url_for('main_routes.index'))