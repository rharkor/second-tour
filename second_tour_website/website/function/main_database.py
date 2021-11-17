import traceback
import logging

from . import main_security
from ..database.main_database import *

def add_account(email, password, user_type_string, output=False):
    hashed_password = main_security.hash_password(password)
    user_type = True if user_type_string == "Administrateur" else False
    user = UTILISATEURS(email, hashed_password, user_type)
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

def delete_account(id):
    try:
        user = UTILISATEURS.query.filter_by(id=id).one()
        # Delete the dependency to
        professeurs = PROFESSEUR.query.filter_by(id_utilisateur=id)
        for a_professeur in professeurs:
            db.session.delete(a_professeur)
        db.session.delete(user)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_serie(serie_choice, specialite1, specialite2):
    try:
        serie = SERIE(serie_choice, specialite1, specialite2)
        if not serie.unvalid:
            db.session.add(serie)
            db.session.commit()
            logging.warning('La série a bien été créée')
            return ['La série a bien été créée', 'success']
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
        matiere = MATIERES(serie, name, name_complete, temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge)
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
        professeur = PROFESSEUR.query.filter_by(matiere=id)
        for a_prof in professeur:
            db.session.delete(a_prof)
        # Delete the dependency
        creneaux = CRENEAU.query.filter_by(id_matiere=id)
        for creneau in creneaux:
            db.session.delete(creneau)
        # Delete the dependency
        matieres1 = CHOIX_MATIERE.query.filter_by(matiere1=id)
        for matiere_actual in matieres1:
            db.session.delete(matiere_actual)
        # Delete the dependency
        matieres2 = CHOIX_MATIERE.query.filter_by(matiere2=id)
        for matiere_actual in matieres2:
            db.session.delete(matiere_actual)
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
        rows_changed = PROFESSEUR.query.filter_by(salle=id).update(dict(salle = None))
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

def add_professeur(email, password, nom, prenom, matiere, salle):
    try:
        user = add_account(email, password, 'Professeur', output=True)
        if user[1][1] == 'danger':
            return user[1]
        user = user[0]
        professeur = PROFESSEUR(user.id, nom, prenom, matiere, salle)
        if not professeur.unvalid:
            db.session.add(professeur)
            db.session.commit()
            logging.warning('Le professeur a bien été crée')
            return ['Le professeur a bien été crée', 'success']
        else:
            return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_professeur_wep(user, nom, prenom, matiere, salle):
    try:
        professeur = PROFESSEUR(user, nom, prenom, matiere, salle)
        if not professeur.unvalid:
            db.session.add(professeur)
            db.session.commit()
            logging.warning('Le professeur a bien été crée')
            return ['Le professeur a bien été crée', 'success']
        else:
            return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_professeur(id):
    try:
        professeur = PROFESSEUR.query.filter_by(id_professeur=id).one()
        # Delete the dependency
        user = UTILISATEURS.query.filter_by(id=professeur.id_utilisateur)
        for an_user in user:
            db.session.delete(an_user)
        db.session.delete(professeur)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_candidat(nom, prenom, id_serie, tiers_temps, output=False):
    try:
        candidat = CANDIDATS(nom, prenom, id_serie, True if tiers_temps == "True" else False)
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
        creneaus = CRENEAU.query.filter_by(id_candidat=id)
        for creneau in creneaus:
            db.session.delete(creneau)
        db.session.delete(candidat)
        db.session.commit()
        return False
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
        choix_matiere = CHOIX_MATIERE.query.filter_by(id_choix_matiere=id).one()
        db.session.delete(choix_matiere)
        db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_creneau(id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin):
    try:
        logging.warning("new Créneau : ", id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin)
        creneau = CRENEAU(id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin)
        if not creneau.unvalid:
            db.session.add(creneau)
            db.session.commit()
            logging.warning('Le créneau a correctement été crée')
            return ['Le créneau a correctement été crée', 'success']
        else:
            return creneau.unvalid
    except Exception:
        logging.warning(traceback.format_exc())
        logging.warning('Erreur : ' + traceback.format_exc())
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


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict
