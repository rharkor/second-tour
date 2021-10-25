from ..main_database import db

class UTILISATEURS(db.Model):
    __tablename__ = 'UTILISATEURS'
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    admin = db.Column(db.Boolean(False))
    __table_args__ = (
        db.UniqueConstraint('email', 'password', 'admin', name='unq_email_password_admin'),
        )

    def __init__(self, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin