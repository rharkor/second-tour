import traceback

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
                return (user, ['L\'utilisateur à bien été crée', 'success'])
            return ['L\'utilisateur à bien été crée', 'success']
        else:
            if output:
                return (user, user.unvalid)
            return user.unvalid
    except Exception:
        if output:
                return (user, ['Erreur : ' + traceback.print_exc(), 'danger'])
        return ['Erreur : ' + traceback.print_exc(), 'danger']

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
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_serie(serie_choice, specialite1, specialite2):
    try:
        serie = SERIE(serie_choice, specialite1, specialite2)
        if not serie.unvalid:
            db.session.add(serie)
            db.session.commit()
            return ['La série à bien été crée', 'success']
        else:
            return serie.unvalid
    except Exception:
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
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_matiere(name, serie, temps_preparation, temps_passage, loge):
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
            print(f"Erreur : No serie found at this id ({serie})")
        name_complete = f"{name} - {serie_name}"
        matiere = MATIERES(serie, name, name_complete, temps_preparation, temps_passage, loge)
        if not matiere.unvalid:
            db.session.add(matiere)
            db.session.commit()
            return ['La matière à bien été crée', 'success']
        else:
            return matiere.unvalid
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_matiere(id):
    try:
        matiere = MATIERES.query.filter_by(id_matiere=id).one()
        # Delete the dependency
        professeur = PROFESSEUR.query.filter_by(matiere=id)
        for a_prof in professeur:
            db.session.delete(a_prof)
        # Delete the dependency
        crenauds = CRENEAU.query.filter_by(id_matiere=id)
        for creneau in crenauds:
            db.session.delete(creneau)
        # Delete the dependency
        matieres1 = CHOIX_MATIERE.query.filter_by(matiere1=id)
        for matiere in matieres1:
            db.session.delete(matiere)
        # Delete the dependency
        matieres2 = CHOIX_MATIERE.query.filter_by(matiere2=id)
        for matiere in matieres2:
            db.session.delete(matiere)
        db.session.delete(matiere)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_salle(numero):
    try:
        salle = SALLE(numero)
        if not salle.unvalid:
            db.session.add(salle)
            db.session.commit()
            return ['La salle à bien été crée', 'success']
        else:
            return salle.unvalid
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_salle(id):
    try:
        salle = SALLE.query.filter_by(id_salle=id).one()
        # Delete the dependency
        professeurs = PROFESSEUR.query.filter_by(salle=id)
        for prof in professeurs:
            db.session.delete(prof)
        # Delete the dependency
        crenauds = CRENEAU.query.filter_by(id_salle=id)
        for creneau in crenauds:
            db.session.delete(creneau)
        # Delete the dependency
        matieres = MATIERES.query.filter_by(loge=id)
        for matiere in matieres:
            db.session.delete(matiere)
        db.session.delete(salle)
        db.session.commit()
        return False
    except Exception:
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
            return ['Le professeur à bien été crée', 'success']
        else:
            return professeur.unvalid
    except Exception:
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
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_candidat(nom, prenom, id_serie, output=False):
    try:
        candidat = CANDIDATS(nom, prenom, id_serie)
        if not candidat.unvalid:
            db.session.add(candidat)
            db.session.commit()
            if output:
                return (candidat, ['Le candidat à bien été crée', 'success'])
            return ['Le candidat à bien été crée', 'success']
        else:
            if output:
                return (candidat, candidat.unvalid)
            return candidat.unvalid
    except Exception:
        if output:
            return (candidat, ['Erreur : ' + traceback.format_exc(), 'danger'])
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_candidat(id):
    try:
        candidat = CANDIDATS.query.filter_by(id_candidat=id).one()
        # Delete the dependency
        choix_matiere = CHOIX_MATIERE.query.filter_by(id_candidat=id)
        for choix in choix_matiere:
            db.session.delete(choix)
        # Delete the dependency
        crenauds = CRENEAU.query.filter_by(id_candidat=id)
        for creneau in crenauds:
            db.session.delete(creneau)
        db.session.delete(candidat)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_choix_matiere(id_candidat, matiere1, matiere2):
    try:
        choix_matiere = CHOIX_MATIERE(id_candidat, matiere1, matiere2)
        if not choix_matiere.unvalid:
            db.session.add(choix_matiere)
            db.session.commit()
            return ['Les choix du candidat on bien été crée', 'success']
        else:
            return choix_matiere.unvalid
    except Exception:
        print(traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_choix_matiere(id):
    try:
        choix_matiere = CHOIX_MATIERE.query.filter_by(id_choix_matiere=id).one()
        db.session.delete(choix_matiere)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_crenaud(id_candidat, id_matiere, id_salle, debut_preparation, fin):
    try:
        print("new Créneau : ", id_candidat, id_matiere, id_salle, debut_preparation, fin)
        creneau = CRENEAU(id_candidat, id_matiere, id_salle, debut_preparation, fin)
        if not creneau.unvalid:
            db.session.add(creneau)
            db.session.commit()
            return ['Le crénaud à correctement été crée', 'success']
        else:
            return creneau.unvalid
    except Exception:
        print(traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_crenaud(id):
    try:
        creneau = CRENEAU.query.filter_by(id_crenaud=id).one()
        db.session.delete(creneau)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']
