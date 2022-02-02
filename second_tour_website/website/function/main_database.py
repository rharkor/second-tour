from datetime import datetime
import traceback
import logging

from flask.helpers import flash

from . import main_security
from ..database.main_database import *

from . import main_email


def add_account(email, password, user_type_string, output=False, id_prof=None):
    hashed_password = main_security.hash_password(password)
    user_type = True if user_type_string == "Administrateur" else False
    user = UTILISATEURS(email, hashed_password, user_type, id_prof)
    try:
        if not user.unvalid:
            db.session.add(user)
            db.session.commit()
            if output:
                logging.warning('L\'utilisateur a bien été crée')
                return (user, ['L\'utilisateur a bien été crée', 'success'])
            logging.warning('L\'utilisateur a bien été crée')
            return ['L\'utilisateur a bien été crée', 'success']
        else:
            if output:
                return (user, user.unvalid)
            return user.unvalid
    except Exception:
        if output:
            logging.warning('Erreur : ' + traceback.logging.warning_exc())
            return (user, ['Erreur : ' + traceback.logging.warning_exc(), 'danger'])
        logging.warning('Erreur : ' + traceback.logging.warning_exc())
        return ['Erreur : ' + traceback.logging.warning_exc(), 'danger']
    
def add_account_token(email, token, user_type_string, id_prof):
    # Token creation
    user_type = True if user_type_string == "Administrateur" else False
    add_token(email, token, user_type, id_prof)
    logging.warning('Le token a bien été crée')
    return ['L\'email à bien été envoyé', 'success']


def delete_account(id):
    try:
        user = UTILISATEURS.query.filter_by(id=id).one()
        if user.admin == False:
            db.session.delete(user)
            db.session.commit()
            return False
        else:
            logging.warning('Impossible de supprimer cet utilisateur')
            return ['Impossible de supprimer cet utilisateur', 'danger']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_serie(serie_choice, specialite1, specialite2, ret=False):
    try:
        serie = SERIE(serie_choice, specialite1, specialite2)
        if not serie.unvalid:
            db.session.add(serie)
            db.session.commit()
            logging.warning('La série a bien été créée')
            if not ret:
                return [['La série a bien été créée', 'success']]
            else:
                return [['La série a bien été créée', 'success'], serie]
        else:
            return serie.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_serie(id):
    try:
        user = SERIE.query.filter_by(id_serie=id).one()
        # Delete the dependency
        matieres = MATIERES.query.filter_by(id_serie=id)
        for matiere in matieres:
            db.session.delete(matiere)
        candidats = CANDIDATS.query.filter_by(id_serie=id)
        for candidat in candidats:
            db.session.delete(candidat)
        db.session.delete(user)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_matiere(name, serie, temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge):
    try:
        serie = int(serie)
        all_series = SERIE.query.all()
        serie_name = None
        for a_serie in all_series:
            if a_serie.id_serie == serie:
                serie_name = a_serie.specialite1
                if a_serie.specialite2 is not None:
                    serie_name += '/' + a_serie.specialite2
        if serie_name is None:
            logging.warning(f"Erreur : No serie found at this id ({serie})")
        name_complete = f"{name} - {serie_name}"
        matiere = MATIERES(serie, name, name_complete, temps_preparation,
                           temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge)
        if not matiere.unvalid:
            db.session.add(matiere)
            db.session.commit()
            logging.warning('La matière a bien été créée')
            return ['La matière a bien été créée', 'success']
        else:
            return matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_matiere(id):
    try:
        matiere = MATIERES.query.filter_by(id_matiere=id).one()
        # Delete the dependency
        liste_matieres = LISTE_MATIERE.query.filter_by(id_matiere=id)
        for liste_matiere in liste_matieres:
            db.session.delete(liste_matiere)
        # Delete the dependency
        creneaux = CRENEAU.query.filter_by(id_matiere=id)
        for creneau in creneaux:
            db.session.delete(creneau)
        # Delete the dependency
        matieres1 = CHOIX_MATIERE.query.filter_by(matiere1=id)
        for matiere_actual in matieres1:
            matiere_actual.matiere1 = None
        # Delete the dependency
        matieres2 = CHOIX_MATIERE.query.filter_by(matiere2=id)
        for matiere_actual in matieres2:
            matiere_actual.matiere2 = None
        db.session.delete(matiere)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_salle(numero):
    try:
        salle = SALLE(numero)
        if not salle.unvalid:
            db.session.add(salle)
            db.session.commit()
            logging.warning('La salle a bien été crée')
            return ['La salle a bien été crée', 'success']
        else:
            return salle.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_salle(id):
    try:
        salle = SALLE.query.filter_by(id_salle=id).one()
        # Delete the dependency
        rows_changed = PROFESSEUR.query.filter_by(
            salle=id).update(dict(salle=None))
        db.session.commit()
        # Delete the dependency
        creneaux = CRENEAU.query.filter_by(id_salle=id)
        for creneau in creneaux:
            db.session.delete(creneau)
        # Delete the dependency
        matieres = MATIERES.query.filter_by(loge=id)
        for matiere in matieres:
            db.session.delete(matiere)
        db.session.delete(salle)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_token(email, token, admin, id_prof):
    token_db = TOKEN(email, str(token), id_prof, admin)
    db.session.add(token_db)
    db.session.commit()
    main_email.send_email(email, token)

def delete_token(token):
    token_db = TOKEN.query.filter_by(token=token).one()
    db.session.delete(token_db)
    db.session.commit()


def add_professeur(email, nom, prenom, salle, matieres=None, token=None, admin=False):
    try:
        # user = add_account(email, 'test123', 'Professeur',
        #                    output=True, id_prof=1)

        # if user[1][1] == 'danger':
        #     return user[1]
        # user = user[0]
        professeur = PROFESSEUR(nom, prenom, salle)
        if not professeur.unvalid:
            db.session.add(professeur)
            db.session.commit()
            logging.warning('Le professeur a bien été crée')

            # Token creation
            add_token(email, token, admin, professeur.id_professeur)
            logging.warning('Le token a bien été crée')

            if matieres:
                for matiere in matieres:
                    liste_matiere = LISTE_MATIERE(
                        professeur.id_professeur, matiere)
                    if not liste_matiere.unvalid:
                        db.session.add(liste_matiere)
                        db.session.commit()
                        logging.warning('La liste matière à bien été ajoutée')

            return ['Le professeur a bien été crée', 'success']
        else:
            return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_professeur_wep(user, nom, prenom, salle, matieres=None):
    try:
        professeur = PROFESSEUR(nom, prenom, salle)
        user_c = UTILISATEURS.query.filter_by(id=user).first()
        user_c.id_professeur = professeur.id_professeur
        if not professeur.unvalid:
            db.session.add(professeur)
            db.session.commit()
            logging.warning('Le professeur a bien été crée')

            if matieres:
                for matiere in matieres:
                    liste_matiere = LISTE_MATIERE(
                        professeur.id_professeur, matiere)
                    if not liste_matiere.unvalid:
                        db.session.add(liste_matiere)
                        db.session.commit()
                        logging.warning('La liste matière à bien été ajoutée')

            return ['Le professeur a bien été crée', 'success']
        else:
            return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def update_professeur_wep(id, user, nom, prenom, salle, matieres=None):
    try:
        
        
        professeur = PROFESSEUR.query.filter_by(id_professeur=id).first()
        if professeur:
            professeur.id_utilisateur = user
            professeur.nom = nom
            professeur.prenom = prenom
            professeur.salle = salle if salle else None

            logging.warning('Le professeur a bien été trouvé')

            delete_liste_matiere_by_prof_id(id)

            if matieres:
                for matiere in matieres:
                    liste_matiere = LISTE_MATIERE(
                        professeur.id_professeur, matiere)
                    if not liste_matiere.unvalid:
                        db.session.add(liste_matiere)
                        logging.warning('La liste matière à bien été ajoutée')

            db.session.commit()

            return ['Le professeur a bien été modifié', 'success']
        else:
            return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_liste_matiere_by_prof_id(id_professeur):
    all_liste_matiere = LISTE_MATIERE.query.filter_by(
        id_professeur=id_professeur).all()
    for liste_matiere in all_liste_matiere:
        db.session.delete(liste_matiere)


def delete_professeur(id):
    try:
        professeur = PROFESSEUR.query.filter_by(id_professeur=id).one()

        liste_matieres = LISTE_MATIERE.query.filter_by(id_professeur=id)
        for liste_matiere in liste_matieres:
            db.session.delete(liste_matiere)

        accounts = UTILISATEURS.query.filter_by(
            id_professeur=professeur.id_professeur)
        for account in accounts:
            db.session.delete(account)

        db.session.delete(professeur)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_candidat(nom, prenom, id_serie, tiers_temps, absent, output=False):
    try:
        candidat = CANDIDATS(nom, prenom, id_serie,
                             True if tiers_temps == "True" else False, True if absent == "True" else False)
        if not candidat.unvalid:
            db.session.add(candidat)
            db.session.commit()
            if output:
                logging.warning('Le candidat a bien été crée')
                return [candidat, 'Le candidat a bien été crée', 'success']
            return ['Le candidat a bien été crée', 'success']
        else:
            if output:
                return (candidat, candidat.unvalid)
            return candidat.unvalid
    except Exception:
        if output:
            logging.warning('Erreur : ' + traceback.format_exc())
            return [candidat, 'Erreur : ' + traceback.format_exc(), 'danger']
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_candidat(id):
    try:
        candidat = CANDIDATS.query.filter_by(id_candidat=id).one()
        # Delete the dependency
        choix_matiere = CHOIX_MATIERE.query.filter_by(id_candidat=id)
        for choix in choix_matiere:
            db.session.delete(choix)
        # Delete the dependency
        creneaux = CRENEAU.query.filter_by(id_candidat=id)
        for creneau in creneaux:
            db.session.delete(creneau)
        db.session.delete(candidat)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_all_candidats():
    try:
        candidats = CANDIDATS.query.all()
        for candidat in candidats:
            logging.warning(f'Suppression du candidat {candidat.id_candidat}')
            result = delete_candidat(candidat.id_candidat)
            if result:
                flash(result[0], result[1])
        return ['Tous les candidats ont correctement été supprimés !', 'success']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_choix_matiere(id_candidat, matiere1, matiere2):
    try:
        choix_matiere = CHOIX_MATIERE(id_candidat, matiere1, matiere2)
        if not choix_matiere.unvalid:
            db.session.add(choix_matiere)
            db.session.commit()
            logging.warning('Les choix du candidat ont bien été crées')
            return ['Les choix du candidat ont bien été crées', 'success']
        else:
            return choix_matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_choix_matiere(id):
    try:
        choix_matiere = CHOIX_MATIERE.query.filter_by(
            id_choix_matiere=id).one()
        db.session.delete(choix_matiere)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_creneau(id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin, auto_commit=True):
    try:
        if type(debut_preparation) == str:
            debut_preparation = datetime.strptime(
                debut_preparation, '%Y/%m/%d:%H:%M')
            fin_preparation = datetime.strptime(
                fin_preparation, '%Y/%m/%d:%H:%M')
            fin = datetime.strptime(fin, '%Y/%m/%d:%H:%M')
        logging.warning("new Créneau : " + str(id_candidat) +
                        " | " + str(id_matiere) + " | " + str(id_salle))
        creneau = CRENEAU(id_candidat, id_matiere, id_salle,
                          debut_preparation, fin_preparation, fin)
        if not creneau.unvalid:
            db.session.add(creneau)
            if auto_commit:
                db.session.commit()
            logging.warning('Le créneau a correctement été crée')
            return ['Le créneau a correctement été crée', 'success']
        else:
            return creneau.unvalid
    except Exception:
        logging.warning(traceback.format_exc())
        logging.warning('Erreur : ' + traceback.format_exc())
        traceback.print_exc()
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_creneau(id):
    try:
        creneau = CRENEAU.query.filter_by(id_creneau=id).one()
        db.session.delete(creneau)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_all_creneaux():
    try:
        creneau = CRENEAU.query.all()
        for creneau in creneau:
            logging.warning(f'Suppression des creneaux {creneau.id_creneau}')
            result = delete_creneau(creneau.id_creneau)
            if result:
                flash(result[0], result[1])
        return ['Tous les créneaux ont correctement été supprimés !', 'success']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_liste_matiere(id_professeur, id_matiere):
    try:
        liste_matiere = LISTE_MATIERE(id_professeur, id_matiere)
        if not liste_matiere.unvalid:
            db.session.add(liste_matiere)
            db.session.commit()
            logging.warning('La matière du professeur à bien été ajouté')
            return ['La matière du professeur à bien été ajouté', 'success']
        else:
            return liste_matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_liste_matiere(id_liste_matiere):
    try:
        liste_matiere = LISTE_MATIERE.query.filter_by(
            id_liste_matiere=id_liste_matiere).one()
        db.session.delete(liste_matiere)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict
