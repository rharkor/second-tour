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

@admin_routes.route('/salles', methods=['POST', 'GET'])
def salles():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'numero' in form:
                    result = main_database.add_salle(form['numero'])
                    flash(result[0], result[1])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_salle(form['id']):
                        flash(r[0], r[1])
        all_salles = SALLE.query.all()
        return render_template('admin/salles.html', all_salles=all_salles)
    else:
        return redirect(url_for('main_routes.connexion'))
 
@admin_routes.route('/professeurs', methods=['POST', 'GET'])
def professeurs():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'email' in form and 'password' in form and 'name' in form and 'surname' in form and 'matiere' in form and 'salle' in form:
                    result = main_database.add_professeur(form['email'], form['password'], form['name'], form['surname'], form['matiere'], form['salle'])
                    flash(result[0], result[1])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_professeur(form['id']):
                        flash(r[0], r[1])
        all_profs = PROFESSEUR.query.all()
        all_matieres = MATIERES.query.all()
        all_salles = SALLE.query.all()
        return render_template('admin/professeurs.html', all_profs=all_profs, all_matieres=all_matieres, all_salles=all_salles)
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
        
@admin_routes.route('/matieres', methods=['POST', 'GET'])
def matieres():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'name' in form and 'serie' in form and 'temps_preparation' in form and 'temps_passage' in form:
                    result = main_database.add_matiere(form['name'], form['serie'], form['temps_preparation'], form['temps_passage'], form['loge'] if 'loge' in form else None)
                    flash(result[0], result[1])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_matiere(form['id']):
                        return flash(r[0], r[1])
        all_matieres = MATIERES.query.all()
        all_series = SERIE.query.all()
        all_salles = SALLE.query.all()
        return render_template('admin/matieres.html', all_matieres=all_matieres, all_series=all_series, all_salles=all_salles)
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