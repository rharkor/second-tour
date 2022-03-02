from ctypes import resize
from ..main_database import db

class SALLE(db.Model):
    __tablename__ = 'SALLE'
    id_salle = db.Column('id_salle', db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint(numero, name="UNQ_NUMERO"),
    )

    def __init__(self, numero):
        self.unvalid = False

        if res := self.unique_numero(numero):
            self.unvalid = res

        self.numero = numero

    def unique_numero(self, numero):
        salle = SALLE.query.filter_by(numero=numero).first()
        if salle:
            return ["Une salle à déjà le même numéro", "danger"]
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class PROFESSEUR(db.Model):
    __tablename__ = 'PROFESSEUR'
    id_professeur = db.Column('id_professeur', db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    salle = db.Column(db.Integer, db.ForeignKey('SALLE.id_salle'), nullable=True)

    def __init__(self, nom, prenom, salle):
        self.unvalid = False
        self.nom = nom
        self.prenom = prenom
        self.salle = salle

    # def unique_iduser_nom_prenom(self, id_utilisateur, nom, prenom):
    #     professeur = PROFESSEUR.query.filter_by(
    #         id_utilisateur=id_utilisateur, nom=nom, prenom=prenom).first()
    #     if professeur:
    #         return ['Ce professeur existe déjà', 'danger']
    #     return False

    # def foreign_iduser(self, id_utilisateur):
    #     utilisateur = UTILISATEUR.query.filter_by(id=id_utilisateur).first()
    #     if utilisateur:
    #         return False
    #     return ['Aucun utilisateur correspondant', 'danger']

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UTILISATEUR(db.Model):
    __tablename__ = 'UTILISATEUR'
    id_UTILISATEUR = db.Column('id_utilisateur', db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean(False), nullable=False)
    id_professeur = db.Column(db.Integer, db.ForeignKey('PROFESSEUR.id_professeur'), nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint(email, admin, name="UNQ_UTILISATEUR_email"),
    )

    def __init__(self, email, password, admin, id_professeur):
        self.unvalid = False

        if res := self.unique_email_admin(email, admin):
            self.unvalid = res
        if res := self.test_id_prof(admin, id_professeur):
            self.unvalid = res

        self.email = email
        self.password = password
        self.admin = admin
        self.id_professeur = id_professeur

    def unique_email_admin(self, email, admin):
        user = UTILISATEUR.query.filter_by(email=email, admin=admin).first()
        if user:
            return ["Cet utilisateur existe déjà", "danger"]
        return False

    def test_id_prof(self, admin, id_prof):
        if not admin and id_prof is None:
            return ["Veuillez spécifier un id professeur", "danger"]
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SERIE(db.Model):
    __tablename__ = 'SERIE'
    id_serie = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), nullable=False)
    specialite1 = db.Column(db.String(50), nullable=False)
    specialite2 = db.Column(db.String(50), nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint(nom, specialite1, specialite2, name="UNQ_NOM_SPE1_SPE2"),
    )

    def __init__(self, nom, specialite1, specialite2=None):
        self.unvalid = False

        if res := self.unique_nom_spe1_spe2(nom, specialite1, specialite2):
            self.unvalid = res

        self.nom = nom
        self.specialite1 = specialite1
        self.specialite2 = specialite2

    def unique_nom_spe1_spe2(self, nom, spe1, spe2):
        serie = SERIE.query.filter_by(
            nom=nom, specialite1=spe1, specialite2=spe2).first()
        if serie:
            return ["Cette serie existe déja", "danger"]
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MATIERE(db.Model):
    __tablename__ = 'MATIERE'
    id_matiere = db.Column(db.Integer, primary_key=True)
    id_serie = db.Column(db.Integer, db.ForeignKey('SERIE.id_serie'), nullable=False)
    nom = db.Column(db.String(30), nullable=False)
    nom_complet = db.Column(db.String(60), nullable=False)
    temps_preparation = db.Column(db.Integer, nullable=False)
    temps_preparation_tiers_temps = db.Column(db.Integer, nullable=False)
    temps_passage = db.Column(db.Integer, nullable=False)
    temps_passage_tiers_temps = db.Column(db.Integer, nullable=False)
    loge = db.Column(db.Integer, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint(nom, nom_complet, temps_preparation, temps_passage, name="UNQ_NOM_NOMCOMP_TPS_PREPA"),
    )

    def __init__(self, id_serie, nom, nom_complet, temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge=None):
        self.unvalid = False

        if res := self.unique_nom_nom_comp_tps_prepa(nom, nom_complet, temps_preparation, temps_passage):
            self.unvalid = res
        if res := self.foreign_serie(id_serie):
            self.unvalid = res

        self.id_serie = id_serie
        self.nom = nom
        self.nom_complet = nom_complet
        self.temps_preparation = temps_preparation
        self.temps_preparation_tiers_temps = temps_preparation_tiers_temps
        self.temps_passage = temps_passage
        self.temps_passage_tiers_temps = temps_passage_tiers_temps
        self.loge = loge

    def unique_nom_nom_comp_tps_prepa(self, nom, nom_complet, tpsprepa, tpspassage):
        matiere = MATIERE.query.filter_by(
            nom=nom, nom_complet=nom_complet, temps_preparation=tpsprepa, temps_passage=tpspassage).first()
        if matiere:
            return ["Cette matière existe déja", "danger"]
        return False

    def foreign_serie(self, id_serie):
        serie = SERIE.query.filter_by(id_serie=id_serie).first()
        if serie:
            return False
        return ["Aucune série ne correspond", "danger"]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class LISTE_MATIERE(db.Model):
    __tablename__ = 'LISTE_MATIERE'
    id_liste_matiere = db.Column(
        'id_liste_matiere', db.Integer, primary_key=True)
    id_professeur = db.Column(db.Integer, db.ForeignKey('PROFESSEUR.id_professeur'), nullable=False)
    id_matiere = db.Column(db.Integer, db.ForeignKey('MATIERE.id_matiere'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint(id_professeur, id_matiere, name="UNQ_PROFESSEUR_MATIERE"),
    )

    def __init__(self, id_professeur, id_matiere):
        self.unvalid = False

        if res := self.unique_id_professeur_id_matiere(id_professeur, id_matiere):
            self.unvalid = res

        if res := self.foreign_id_professeur(id_professeur):
            self.unvalid = res

        if res := self.foreign_id_matiere(id_matiere):
            self.unvalid = res

        self.id_professeur = id_professeur
        self.id_matiere = id_matiere

    def unique_id_professeur_id_matiere(self, id_professeur, id_matiere):
        liste_matiere = LISTE_MATIERE.query.filter_by(
            id_professeur=id_professeur, id_matiere=id_matiere).first()
        if liste_matiere:
            return ['Cette liste matiere existe déjà', 'danger']
        return False

    def foreign_id_professeur(self, id_professeur):
        professeur = PROFESSEUR.query.filter_by(
            id_professeur=id_professeur).first()
        if professeur:
            return False
        return ['Aucun professeur correspondant', 'danger']

    def foreign_id_matiere(self, id_matiere):
        matiere = MATIERE.query.filter_by(
            id_matiere=id_matiere).first()
        if matiere:
            return False
        return ['Aucune matiere correspondante', 'danger']

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CANDIDAT(db.Model):
    __tablename__ = 'CANDIDAT'
    id_candidat = db.Column('id_candidat', db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(150), nullable=False)
    id_serie = db.Column(db.Integer, db.ForeignKey('SERIE.id_serie'), nullable=False)
    tiers_temps = db.Column(db.Boolean, nullable=False)
    absent = db.Column(db.Boolean, nullable=False)

    def __init__(self, nom, prenom, id_serie, tiers_temps, absent):
        self.unvalid = False

        if res := self.foreign_id_serie(id_serie):
            self.unvalid = res

        self.nom = nom
        self.prenom = prenom
        self.id_serie = id_serie
        self.tiers_temps = tiers_temps
        self.absent = absent

    def foreign_id_serie(self, id_serie):
        serie = SERIE.query.filter_by(id_serie=id_serie).first()
        if serie:
            return False
        return ['Aucune série correspondante', 'danger']

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CHOIX_MATIERE(db.Model):
    __tablename__ = 'CHOIX_MATIERE'
    id_choix_matiere = db.Column(
        'id_choix_matiere', db.Integer, primary_key=True)
    id_candidat = db.Column(db.Integer, db.ForeignKey('CANDIDAT.id_candidat'),  nullable=False)
    matiere1 = db.Column(db.Integer, db.ForeignKey('MATIERE.id_matiere'), nullable=True)
    matiere2 = db.Column(db.Integer, db.ForeignKey('MATIERE.id_matiere'), nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint(id_candidat, name="UNQ_CANDIDAT"),
    )

    def __init__(self, id_candidat, matiere1=None, matiere2=None):
        self.unvalid = False

        if res := self.unique_id_candidat(id_candidat):
            self.unvalid = res
        if res := self.foreign_id_candidat(id_candidat):
            self.unvalid = res
        if res := self.foreign_matiere1(matiere1):
            self.unvalid = res
        if res := self.foreign_matiere2(matiere2):
            self.unvalid = res

        self.id_candidat = id_candidat
        self.matiere1 = matiere1
        self.matiere2 = matiere2

    def unique_id_candidat(self, id_candidat):
        choix_matiere = CHOIX_MATIERE.query.filter_by(
            id_candidat=id_candidat).first()
        if choix_matiere:
            return ['Le choix des matieres pour ce candidat existe déjà', 'danger']
        return False

    def foreign_id_candidat(self, id_candidat):
        candidat = CANDIDAT.query.filter_by(id_candidat=id_candidat).first()
        if candidat:
            return False
        return ['Aucun candidat correspondant', 'danger']

    def foreign_matiere1(self, matiere1):
        if matiere1:
            matiere = MATIERE.query.filter_by(id_matiere=matiere1).first()
            if matiere:
                return False
            return ['Aucune matiere correspondante', 'danger']
        return False

    def foreign_matiere2(self, matiere2):
        if matiere2:
            matiere = MATIERE.query.filter_by(id_matiere=matiere2).first()
            if matiere:
                return False
            return ['Aucune matiere correspondante', 'danger']
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CRENEAU(db.Model):
    __tablename__ = 'CRENEAU'
    id_creneau = db.Column('id_creneau', db.Integer, primary_key=True)
    id_candidat = db.Column(db.Integer, db.ForeignKey('CANDIDAT.id_candidat'), nullable=False)
    id_matiere = db.Column(db.Integer, db.ForeignKey('MATIERE.id_matiere'), nullable=False)
    id_salle = db.Column(db.Integer, db.ForeignKey('SALLE.id_salle'), nullable=False)
    debut_preparation = db.Column(db.DateTime, nullable=False)
    fin_preparation = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint(id_candidat, debut_preparation, name="UNQ_CANDIDAT_PREPA"),
        db.UniqueConstraint(id_candidat, id_matiere, name="UNQ_CANDIDAT_MATIERE"),
    )

    def __init__(self, id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin):
        self.unvalid = False

        if res := self.unique_id_candidat_debut_preparation(id_candidat, debut_preparation):
            self.unvalid = res
        if res := self.unique_id_candidat_matiere(id_candidat, id_matiere):
            self.unvalid = res
        if res := self.foreign_id_candidat(id_candidat):
            self.unvalid = res
        if res := self.foreign_id_matiere(id_matiere):
            self.unvalid = res
        if res := self.foreign_id_salle(id_salle):
            self.unvalid = res

        self.id_candidat = id_candidat
        self.id_matiere = id_matiere
        self.id_salle = id_salle
        self.debut_preparation = debut_preparation
        self.fin_preparation = fin_preparation
        self.fin = fin

    def unique_id_candidat_matiere(self, id_candidat, id_matiere):
        crenaud = CRENEAU.query.filter_by(
            id_candidat=id_candidat, id_matiere=id_matiere).first()
        if crenaud:
            return ["Ce candidat à déjà un crénaud de prévu pour cette matière", "danger"]
        return False

    def unique_id_candidat_debut_preparation(self, id_candidat, debut_preparation):
        crenaud = CRENEAU.query.filter_by(
            id_candidat=id_candidat, debut_preparation=debut_preparation).first()
        if crenaud:
            return ["Ce candidat à déjà un crénaud qui commence à la même heure", "danger"]
        return False

    def foreign_id_candidat(self, id_candidat):
        candidat = CANDIDAT.query.filter_by(id_candidat=id_candidat).first()
        if candidat:
            return False
        return ["Aucun candidat correspondant", "danger"]

    def foreign_id_matiere(self, id_matiere):
        matiere = MATIERE.query.filter_by(id_matiere=id_matiere).first()
        if matiere:
            return False
        return ["Aucune matière correspondante", "danger"]

    def foreign_id_salle(self, id_salle):
        salle = SALLE.query.filter_by(id_salle=id_salle).first()
        if salle:
            return False
        return ["Aucune salle correspondante", "danger"]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TOKEN(db.Model):
    __tablename__ = 'TOKEN'
    __table_args__ = (
        db.UniqueConstraint('token', name='unique_token'),
    )
    
    id_token = db.Column('id_token', db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False)
    id_professeur = db.Column(db.Integer, db.ForeignKey('PROFESSEUR.id_professeur'), nullable=True)
    admin = db.Column(db.Boolean(False), nullable=False)
    # __table_args__ = (
    #     db.UniqueConstraint(email, name="UNQ_UTILISATEUR_email"),
    # )

    def __init__(self, email, token, id_professeur, admin):
        self.unvalid = False

        if res := self.test_id_prof(admin, id_professeur):
            self.unvalid = res

        self.email = email
        self.token = token
        self.id_professeur = id_professeur
        self.admin = admin

    def test_id_prof(self, admin, id_prof):
        if not admin and id_prof is None:
            return ["Veuillez spécifier un id professeur", "danger"]
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class HORAIRE(db.Model):
    __tablename__ = 'HORAIRE'
    id_horaire = db.Column('id_horaire', db.Integer, primary_key=True)
    horaire_arr1 = db.Column(db.DateTime, nullable=False)
    horaire_dep1 = db.Column(db.DateTime, nullable=False)
    horaire_arr2 = db.Column(db.DateTime, nullable=False)
    horaire_dep2 = db.Column(db.DateTime, nullable=False)
    horaire_arr3 = db.Column(db.DateTime, nullable=False)
    horaire_dep3 = db.Column(db.DateTime, nullable=False)
    id_professeur = db.Column(db.Integer, nullable=False)

    def __init__(self, horaire_arr1, horaire_dep1, horaire_arr2, horaire_dep2, horaire_arr3, horaire_dep3, id_professeur):
        self.unvalid = False

        if res := self.unique_id_professeur(id_professeur):
            self.unvalid = res

        if res := self.foreign_id_professeur(id_professeur):
            self.unvalid = res
        
        self.horaire_arr1 = horaire_arr1
        self.horaire_dep1 = horaire_dep1
        self.horaire_arr2 = horaire_arr2
        self.horaire_dep2 = horaire_dep2
        self.horaire_arr3 = horaire_arr3
        self.horaire_dep3 = horaire_dep3
        self.id_professeur = id_professeur


    def unique_id_professeur(self, id_professeur):
        horaire = HORAIRE.query.filter_by(
            id_professeur=id_professeur).first()
        if horaire:
            return ['L\'horaire pour ce professeur existe déjà', 'danger']
        return False


    def foreign_id_professeur(self, id_professeur):
        professeur = PROFESSEUR.query.filter_by(
            id_professeur=id_professeur).first()
        if professeur:
            return False
        return ['Aucun professeur correspondant', 'danger']


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

