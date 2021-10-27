import hashlib
import os

from ..database.main_database import *
 

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    storage = salt + key 
    return storage

def test_password(password, user):
    hashed = user.password
    key = hashed[32:]
    salt = hashed[:32]
    test_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if test_key == key:
        return True
    return False

def test_session_connected(session, admin):
    if 'email' in session and 'password' in session and 'admin' in session:
        user = UTILISATEURS.query.filter_by(email=session['email'], admin=session['admin']).first()
        if user:
            if session['password'] == user.password:
                if admin:
                    return user.admin == True
                else:
                    return True
    return False