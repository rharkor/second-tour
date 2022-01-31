from pbkdf2 import crypt
import os
import traceback

from ..database.main_database import *
 

def hash_password(password):
    key = crypt(password, iterations=1000)
    return key
    
    # return password

def test_password(password, user):
    hashed = user.password
    
    try:
        test_key = crypt(password, hashed, iterations=1000)
    except Exception:
        traceback.print_exc()
    if test_key == hashed:
        return True
    # return False
    return password == user.password

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