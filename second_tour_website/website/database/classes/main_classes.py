from ctypes import resize
from ..main_database import db

class UTILISATEURS(db.Model):
    __tablename__ = 'UTILISATEURS'
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200),nullable=False)
    admin = db.Column(db.Boolean(False), nullable=False)
    # __table_args__ = (
    #     db.UniqueConstraint(email, name="UNQ_UTILISATEURS_email"), 
    # )

    def __init__(self, email, password, admin):
        self.unvalid = False

        if res := self.unique_email_admin(email, admin):
            self.unvalid = res

        self.email = email
        self.password = password
        self.admin = admin

    def unique_email_admin(self, email, admin):
        user = UTILISATEURS.query.filter_by(email=email, admin=admin).first()
        if user:
            return ["Cet utilisateur existe déjà", "danger"]
        return False

class SERIE(db.Model):
    __tablename__=  'SERIE'
    id_serie = db.Column('id', db.Integer, primary_key = True)
    nom = db.Column(db.String(40), nullable=False)
    specialite1 = db.Column(db.String(50),nullable=False)
    specialite2 = db.Column(db.String(50),nullable=True)

    def __init__(self, nom, specialite1, specialite2=None):
        self.unvalid = False

        if res := self.unique_nom_spe1_spe2(nom, specialite1, specialite2):
            self.unvalid = res

        self.nom = nom
        self.specialite1 = specialite1
        self.specialite2 = specialite2

    def unique_nom_spe1_spe2(self, nom, spe1, spe2):
        serie = SERIE.query.filter_by(nom=nom, specialite1=spe1, specialite2=spe2).first()
        if serie:
            return ["Cette serie existe déja", "danger"]
        return False

class MATIERES(db.Model):
    __tablename__= 'MATIERES'
    id_matiere = db.Column('id', db.Integer, primary_key = True)
    id_serie = db.Column(db.Integer, nullable=False)
    nom = db.Column(db.String(30),nullable=False)
    nom_complet = db.Column(db.String(60),nullable=False)
    temps_preparation = db.Column(db.Integer, nullable=False)
    temps_passage = db.Column(db.Integer, nullable=False)
    loge = db.Column(db.Integer, nullable=True)

    def __init__(self, id_serie, nom, nom_complet, temps_preparation, temps_passage, loge=None):
        self.unvalid = False

        if res := self.unique_nom_nom_comp_tps_prepa(nom, nom_complet, temps_preparation, temps_passage):
            self.unvalid = res
        if res := self.foreign_serie(id_serie):
            self.unvalid = res

        self.id_serie = id_serie
        self.nom = nom
        self.nom_complet = nom_complet
        self.temps_preparation = temps_preparation
        self.temps_passage = temps_passage
        self.loge = loge

    def unique_nom_nom_comp_tps_prepa(self, nom, nom_complet, tpsprepa, tpspassage):
        matiere = MATIERES.query.filter_by(nom=nom, nom_complet=nom_complet, temps_preparation=tpsprepa, temps_passage=tpspassage).first()
        if matiere:
            return ["Cette matière existe déja", "danger"]
        return False
    
    def foreign_serie(self, id_serie):
        serie = SERIE.query.filter_by(id_serie=id_serie).first()
        if serie:
            return False
        return ["Aucune série ne correspond", "danger"]

class SALLE(db.Model):
    __tablename__ = 'SALLE'
    id_salle = db.Column('id', db.Integer, primary_key = True)
    numero = db.Column(db.String(50), nullable=False)

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

class PROFESSEUR(db.Model):
    __tablename__ = 'PROFESSEUR'
    id_professeur = db.Column('id', db.Integer, primary_key = True)
    id_utilisateur = db.Column(db.Integer, nullable=False)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    matiere = db.Column(db.Integer, nullable=False)
    salle = db.Column(db.Integer, nullable=False)

    def __init__(self, id_utilisateur, nom, prenom, matiere, salle):
        self.unvalid = False

        if res := self.unique_iduser_nom_prenom_matiere(id_utilisateur, nom, prenom, matiere):
            self.unvalid = res
        if res := self.foreign_iduser(id_utilisateur):
            self.unvalid = res
        if res := self.foreign_matiere(matiere):
            self.unvalid = res

        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.matiere = matiere
        self.salle = salle

    def unique_iduser_nom_prenom_matiere(self, id_utilisateur, nom, prenom, matiere):
        professeur = PROFESSEUR.query.filter_by(id_utilisateur=id_utilisateur, nom=nom, prenom=prenom, matiere=matiere).first()
        if professeur:
            return ['Ce professeur existe déjà', 'danger']
        return False

    def foreign_iduser(self, id_utilisateur):
        utilisateur = UTILISATEURS.query.filter_by(id=id_utilisateur).first()
        if utilisateur:
            return False
        return ['Aucun utilisateur ne correspondant', 'danger']
    
    def foreign_matiere(self, matiere):
        matiere = MATIERES.query.filter_by(id_matiere=matiere).first()
        if matiere:
            return False
        return ['Aucune matière ne correspondantes', 'danger']