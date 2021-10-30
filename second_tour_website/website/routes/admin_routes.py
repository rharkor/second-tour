from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *

admin_routes = Blueprint('admin_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@admin_routes.route('/')
@admin_routes.route('/acceuil', methods=['POST', 'GET'])
def acceuil():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('generate_button') is not None:
                main_calendrier.generation_calendrier()
        all_candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
        all_series = SERIE.query.all()
        all_matieres = MATIERES.query.all()
        all_salles = SALLE.query.all()
        return render_template('admin/acceuil.html', all_candidats=all_candidats, all_creneaux=all_creneaux, all_series=all_series, all_matieres=all_matieres, all_salles=all_salles)
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/candidats', methods=['POST', 'GET'])
def candidats():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'name' in form and 'surname' in form and 'serie' in form:
                    result = main_database.add_candidat(form['name'], form['surname'], form['serie'], output=True)
                    if result[1][1] == 'danger':
                        flash(result[0], result[1])
                    else:
                        if 'matiere1' in form and 'matiere2' in form:
                            if form['matiere1'] or form['matiere2']:
                                second_result = main_database.add_choix_matiere(result[0].id_candidat, form['matiere1'], form['matiere2'])
                                flash(second_result[0], second_result[1])
                            else:
                                flash(result[1][0], result[1][1])
                        else:
                            flash(result[1][0], result[1][1])
                        
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_candidat(form['id']):
                        flash(r[0], r[1])
            elif form.get('modif_button') is not None:
                if 'name' in form and 'surname' in form and 'serie' in form and 'id' in form:
                    if r := main_database.delete_candidat(form['id']):
                        flash(r[0], r[1])
                    else:
                        result = main_database.add_candidat(form['name'], form['surname'], form['serie'], output=True)
                        if result[1][1] == 'danger':
                            flash(result[0], result[1])
                        else:
                            if 'matiere1' in form and 'matiere2' in form:
                                if form['matiere1'] or form['matiere2']:
                                    second_result = main_database.add_choix_matiere(result[0].id_candidat, form['matiere1'], form['matiere2'])
                                    if second_result[1] != 'danger':
                                        flash("Modification correctement effecutée", second_result[1])
                                    else:
                                        flash(second_result[0], second_result[1])
                                else:
                                    flash(result[1][0], result[1][1])
                            else:
                                if result[1][1] != "danger":
                                    flash("Modification correctement effecutée", result[1][1])
                                else:
                                    flash(result[1][0], result[1][1])
        # Serialize TABLE
        candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_candidats = []
        for a_candidat in candidats:
            all_candidats.append(a_candidat.as_dict())
        # Serialize TABLE
        choix_matieres = CHOIX_MATIERE.query.all()
        all_choix_matieres = []
        for a_choix_matiere in choix_matieres:
            all_choix_matieres.append(a_choix_matiere.as_dict())
        # Serialize TABLE
        all_series = []
        series = SERIE.query.all()
        for a_serie in series:
            all_series.append(a_serie.as_dict())
        # Serialize TABLE
        matieres = MATIERES.query.all()
        all_matieres = []
        for a_matiere in matieres:
            all_matieres.append(a_matiere.as_dict())
        
        all_professeurs = PROFESSEUR.query.all()
        all_salles = SALLE.query.all()
        all_creneaux = CRENEAU.query.all()
        return render_template('admin/candidats.html', all_candidats=all_candidats, all_choix_matieres=all_choix_matieres, all_series=all_series, all_matieres=all_matieres, all_professeurs=all_professeurs, all_salles=all_salles, all_creneaux=all_creneaux)
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
        all_profs = PROFESSEUR.query.order_by(PROFESSEUR.nom).all()
        all_matieres = MATIERES.query.all()
        all_creneaux = CRENEAU.query.all()
        all_candidats = CANDIDATS.query.all()
        all_salles = SALLE.query.order_by(SALLE.numero).all()
        return render_template('admin/salles.html', all_salles=all_salles, all_profs=all_profs, all_matieres=all_matieres, all_creneaux=all_creneaux, all_candidats=all_candidats)
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
        all_profs = PROFESSEUR.query.order_by(PROFESSEUR.nom).all()
        all_matieres = MATIERES.query.all()
        all_salles = SALLE.query.all()
        all_creneaux = CRENEAU.query.all()
        all_candidats = CANDIDATS.query.all()
        return render_template('admin/professeurs.html', all_profs=all_profs, all_matieres=all_matieres, all_salles=all_salles,all_creneaux=all_creneaux, all_candidats=all_candidats)
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
                
        all_series = SERIE.query.order_by(SERIE.nom).all()
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
        all_matieres = MATIERES.query.order_by(MATIERES.nom).all()
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