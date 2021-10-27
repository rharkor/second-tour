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
    specialite2 = db.Column(db.String(50),nullable=False)

    def __init__(self, nom, specialite1, specialite2):
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