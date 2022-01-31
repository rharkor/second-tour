import logging
from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from flask.helpers import flash
import pandas as pd
from zipfile import ZipFile
from uuid import uuid4

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *
from ..main_website import app

admin_routes = Blueprint('admin_routes', __name__,
                         template_folder='templates',
                         static_folder='static')


@admin_routes.route('/')
@admin_routes.route('/accueil', methods=['POST', 'GET'])
def accueil():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('generate_button') is not None:
                main_calendrier.generation_calendrier()
            elif form.get('excel_button') is not None:
                filename = app.config['UPLOAD_FOLDER'] + "/donees.xlsx"
                writer = pd.ExcelWriter(filename)
                for table in [CRENEAU, CANDIDATS, PROFESSEUR, SALLE, SERIE, MATIERES, CHOIX_MATIERE, UTILISATEURS]:
                    records = db.session.query(table).all()
                    data_list = [main_database.to_dict(
                        item) for item in records]
                    df = pd.DataFrame(data_list)
                    df.to_excel(writer, sheet_name=table.__table__.name)
                writer.save()
                return send_file(filename)
        else:
            result = main_calendrier.test_calendar_complete()
            flash(result[0], result[1]) if result[1] == "danger" else flash(
                "Le calendrier est complet !    ", result[1])
            logging.warning(result[0] if result[1] ==
                            "danger" else "Le calendrier est complet")
        all_candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
        all_series = SERIE.query.all()
        all_matieres = MATIERES.query.all()
        # Serialize table
        professeurs = PROFESSEUR.query.all()
        all_professeurs = []
        for professeur in professeurs:
            all_professeurs.append(professeur.as_dict())
        # Serialize table
        salles = SALLE.query.all()
        all_salles = []
        for salle in salles:
            all_salles.append(salle.as_dict())
        return render_template('admin/accueil.html', all_professeurs=all_professeurs, all_candidats=all_candidats, all_creneaux=all_creneaux, all_series=all_series, all_matieres=all_matieres, all_salles=all_salles)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/candidats', methods=['POST', 'GET'])
def candidats():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'name' in form and 'surname' in form and 'serie' in form and 'tiers_temps' in form and 'absent' in form:
                    result = main_database.add_candidat(
                        form['name'], form['surname'], form['serie'], form['tiers_temps'], form['absent'], output=True)
                    if result[1][1] == 'danger':
                        flash(result[0], result[1])
                        logging.warning(result[0])
                    else:
                        if 'matiere1' in form and 'matiere2' in form:
                            if form['matiere1'] or form['matiere2']:
                                second_result = main_database.add_choix_matiere(
                                    result[0].id_candidat, form['matiere1'], form['matiere2'])
                                flash(second_result[0], second_result[1])
                                logging.warning(second_result[0])
                            else:
                                flash(result[1][0], result[1][1])
                                logging.warning(result[1][0])
                        else:
                            flash(result[1][0], result[1][1])
                            logging.warning(result[1][0])

            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_candidat(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
            elif form.get('modif_button') is not None:
                if 'name' in form and 'surname' in form and 'serie' in form and 'id' in form and 'tiers_temps' in form and 'absent' in form:
                    if r := main_database.delete_candidat(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
                    else:
                        result = main_database.add_candidat(
                            form['name'], form['surname'], form['serie'], form['tiers_temps'], form['absent'], output=True)
                        if result[1][1] == 'danger':
                            flash(result[0], result[1])
                            logging.warning(resize[0])
                        else:
                            if 'matiere1' in form and 'matiere2' in form:
                                if form['matiere1'] or form['matiere2']:
                                    second_result = main_database.add_choix_matiere(
                                        result[0].id_candidat, form['matiere1'], form['matiere2'])
                                    if second_result[1] != 'danger':
                                        flash(
                                            "Modification correctement effecutée", second_result[1])
                                        logging.warning(
                                            "Modification effectuée")
                                    else:
                                        flash(
                                            second_result[0], second_result[1])
                                        logging.warning(second_result[0])
                                else:
                                    flash(result[1][0], result[1][1])
                                    logging.warning(result[1][0])
                            else:
                                if result[1][1] != "danger":
                                    flash(
                                        "Modification correctement effecutée", result[1][1])
                                    logging.warning("Modification effectuée")
                                else:
                                    flash(result[1][0], result[1][1])
                                    logging.warning(result[1][0])
            elif form.get('delete_all_button') is not None:
                result = main_database.delete_all_candidats()
                flash(result[0], result[1])
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
        all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
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
                    logging.warning(result[0])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_salle(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])

        all_matieres = MATIERES.query.all()
        all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
        # Serialize table
        creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
        all_creneaux = []
        for creneau in creneaux:
            all_creneaux.append(creneau.as_dict())

        all_candidats = CANDIDATS.query.all()

        # Serialize table
        professeurs = PROFESSEUR.query.all()
        all_professeurs = []
        for professeur in professeurs:
            all_professeurs.append(professeur.as_dict())
        # Serialize table
        salles = SALLE.query.all()
        all_salles = []
        for salle in salles:
            all_salles.append(salle.as_dict())

        all_choix_matieres = CHOIX_MATIERE.query.all()
        all_liste_matiere = LISTE_MATIERE.query.all()

        return render_template('admin/salles.html', all_salles=all_salles, all_professeurs=all_professeurs, all_matieres=all_matieres, all_creneaux=all_creneaux, all_candidats=all_candidats, all_choix_matieres=all_choix_matieres, all_liste_matiere=all_liste_matiere)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/professeurs', methods=['POST', 'GET'])
def professeurs():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'email' in form and 'name' in form and 'surname' in form and 'salle' in form:
                    token = uuid4()
                    result = main_database.add_professeur(
                        form['email'], form['name'], form['surname'], form['salle'], form.getlist('matieres[]') if 'matieres[]' in form else [], token)
                    flash(result[0], result[1])
                    logging.warning(result[0])

            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_professeur(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
            elif form.get('modify_button') is not None:
                if 'user' in form and 'prof_id' in form and 'name' in form and 'surname' in form and 'salle' in form:
                    # result = main_database.delete_professeur(form['prof_id'])
                    result = main_database.update_professeur_wep(form['prof_id'], form['user'],
                                                                 form['name'], form['surname'], form['salle'], form.getlist('matieres[]') if 'matieres[]' in form else [])
                    flash(result[0], result[1])
                    logging.warning(result[0])
                    print(form)

        # Serialize PROFESSEUR
        profs = PROFESSEUR.query.order_by(PROFESSEUR.nom).all()
        all_profs = []
        for a_professeur in profs:
            all_profs.append(a_professeur.as_dict())
        # Serialize TABLE
        matieres = MATIERES.query.all()
        all_matieres = []
        for a_matiere in matieres:
            all_matieres.append(a_matiere.as_dict())
        all_salles = SALLE.query.all()
        all_creneaux = CRENEAU.query.order_by(CRENEAU.debut_preparation).all()
        all_candidats = CANDIDATS.query.all()

        all_horaires = HORAIRES.query.all()

        liste_matieres = LISTE_MATIERE.query.all()
        all_liste_matiere = []
        for liste_matiere in liste_matieres:
            all_liste_matiere.append(liste_matiere.as_dict())
        return render_template('admin/professeurs.html', all_profs=all_profs, all_matieres=all_matieres, all_salles=all_salles, all_creneaux=all_creneaux, all_candidats=all_candidats, all_liste_matiere=all_liste_matiere, all_horaires=all_horaires)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/series', methods=['POST', 'GET'])
def series():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'serie' in form and 'specialite1' in form:
                    result = main_database.add_serie(
                        form['serie'], form['specialite1'], form['specialite2'] if 'specialite2' in form else None, True)
                    flash(result[0][0], result[0][1])
                    logging.warning(result[0][0])
                    if result[0][1] == 'success':
                        result_s = main_database.add_matiere(
                            'Français', result[1].id_serie, 30, 40, 30, 40, None)
                        logging.warning(result_s[0])
                        result_s = main_database.add_matiere(
                            'Philosophie', result[1].id_serie, 30, 40, 30, 40, None)
                        logging.warning(result_s[0])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_serie(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])

        all_series = SERIE.query.order_by(SERIE.nom).all()
        all_candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_salle = SALLE.query.all()
        all_matieres = MATIERES.query.all()
        all_choix_matieres = CHOIX_MATIERE.query.all()
        return render_template('admin/series.html', all_series=all_series, all_candidats=all_candidats, all_salle=all_salle, all_matieres=all_matieres, all_choix_matieres=all_choix_matieres)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/matieres', methods=['POST', 'GET'])
def matieres():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                if 'name' in form and 'serie' in form and 'temps_preparation' in form and 'temps_passage' in form and 'temps_preparation_tiers_temps' in form and 'temps_passage_tiers_temps' in form:
                    result = main_database.add_matiere(
                        form['name'], form['serie'], form['temps_preparation'], form['temps_preparation_tiers_temps'], form['temps_passage'], form['temps_passage_tiers_temps'], form['loge'] if 'loge' in form else None)
                    flash(result[0], result[1])
                    logging.warning(result[0])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_matiere(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
        all_matieres = MATIERES.query.order_by(MATIERES.nom).all()
        all_series = SERIE.query.all()
        all_salles = SALLE.query.all()
        all_candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_choix_matieres = CHOIX_MATIERE.query.all()
        return render_template('admin/matieres.html', all_matieres=all_matieres, all_series=all_series, all_salles=all_salles, all_candidats=all_candidats, all_choix_matieres=all_choix_matieres)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/comptes', methods=['POST', 'GET'])
def comptes():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            if form.get('submit_button') is not None:
                print(form)
                if 'email' in form and 'type' in form and 'prof' in form:
                    result = main_database.add_account_token(
                        form['email'], uuid4(), form['type'], form['prof'])
                    flash(result[0], result[1])
                    logging.warning(result[0])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if r := main_database.delete_account(form['id']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
            elif form.get('delete_button_token') is not None:
                if 'token' in form:
                    if r := main_database.delete_token(form['token']):
                        flash(r[0], r[1])
                        logging.warning(r[0])
        all_users = UTILISATEURS.query.all()
        all_tokens = TOKEN.query.all()
        all_professeurs = PROFESSEUR.query.all()
        return render_template('admin/comptes.html', all_users=all_users, all_tokens=all_tokens, all_professeurs=all_professeurs)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/creneau', methods=['POST', 'GET'])
def creneau():
    if main_security.test_session_connected(session, True):
        if request.method == 'POST':
            form = request.form
            print(form)
            if form.get('submit_button') is not None:
                if 'candidat' in form and 'matiere' in form and 'salle' in form and 'debut' in form and 'fin_prepa' in form and 'fin' in form:
                    result = main_database.add_creneau(
                        form['candidat'], form['matiere'], form['salle'], form['debut'], form["fin_prepa"], form['fin'])
                    flash(result[0], result[1])
                    logging.warning(result[0])
            elif form.get('modify_button') is not None:
                if 'last_creneau_id' in form and 'candidat' in form and 'matiere' in form and 'salle' in form and 'debut' and 'fin_prepa' in form in form and 'fin' in form:
                    if not (res := main_database.delete_creneau(form['last_creneau_id'])):
                        result = main_database.add_creneau(
                            form['candidat'], form['matiere'], form['salle'], form['debut'], form["fin_prepa"], form['fin'])
                        flash(result[0], result[1])
                        logging.warning(result[0])
                    else:
                        flash(res[0], res[1])
                        logging.warning(res[0])
            elif form.get('delete_button') is not None:
                if 'id' in form:
                    if (res := main_database.delete_creneau(form['id'])):
                        flash(res[0], res[1])
                        logging.warning(res[0])
                    else:
                        flash("Le créneau à bien été supprimé", "success")
                        logging.warning("Le créneau à bien été supprimé")
            elif form.get('delete_all_button') is not None:
                result = main_database.delete_all_creneaux()
                flash(result[0], result[1])

        # Serialize table
        creneaux = CRENEAU.query.order_by(CRENEAU.id_candidat).all()
        all_creneau = []
        for creneau in creneaux:
            all_creneau.append(creneau.as_dict())
        all_creneau_deb = CRENEAU.query.order_by(
            CRENEAU.debut_preparation).all()
        # Serialize table
        candidats = CANDIDATS.query.order_by(CANDIDATS.nom).all()
        all_candidats = []
        for candidat in candidats:
            all_candidats.append(candidat.as_dict())
        # Serialize table
        matieres = MATIERES.query.all()
        all_matieres = []
        for a_matiere in matieres:
            all_matieres.append(a_matiere.as_dict())
        # Serialize table
        salles = SALLE.query.all()
        all_salles = []
        for salle in salles:
            all_salles.append(salle.as_dict())
        # Serialize table
        choix_matieres = CHOIX_MATIERE.query.all()
        all_choix_matieres = []
        for choix_matiere in choix_matieres:
            all_choix_matieres.append(choix_matiere.as_dict())
        # Serialize table
        series = SERIE.query.all()
        all_series = []
        for serie in series:
            all_series.append(serie.as_dict())
        # Serialize table
        professeurs = PROFESSEUR.query.all()
        all_professeur = []
        for professeur in professeurs:
            all_professeur.append(professeur.as_dict())

        liste_matieres = LISTE_MATIERE.query.all()
        all_liste_matieres = []
        for liste_matiere in liste_matieres:
            all_liste_matieres.append(liste_matiere.as_dict())
        return render_template('admin/creneau.html', all_professeur=all_professeur, all_creneau=all_creneau, all_candidats=all_candidats, all_matieres=all_matieres, all_salles=all_salles, all_creneau_deb=all_creneau_deb, all_series=all_series, all_choix_matieres=all_choix_matieres, all_liste_matieres=all_liste_matieres)
    else:
        return redirect(url_for('main_routes.connexion'))


@admin_routes.route('/deconnexion')
def deconnexion():
    if session['email']:
        session.pop('email', None)
    if session['password']:
        session.pop('password', None)
    flash('Vous avez correment été déconnecté', 'primary')
    logging.warning('Vous avez correctement été déconnecté')
    return redirect(url_for('main_routes.index'))
