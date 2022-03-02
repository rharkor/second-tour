from flask import flash
from pbkdf2 import crypt
import os
import traceback
import logging

from ..database.main_database import *
 

def hash_password(password):
    key = crypt(password, iterations=1000)
    return key
    
    # return password

def test_password(password, user):
        
    hashed = user['password']    
    try:
        test_key = crypt(password, hashed, iterations=1000)
    except Exception:
        traceback.print_exc()
            
    if test_key == hashed:
        return True
    # return False
    return password == hashed

def test_session_connected(session, admin):
    if 'email' in session and 'password' in session and 'admin' in session:
        response = ask_api("data/fetchfilter/utilisateur", {"email": session["email"], "admin": str(session["admin"]).lower()})
        if response.status_code != 200:
            flash("Une erreur est survenue lors de la récupérations des utilisateurs", "danger")
            return False
        user = response.json()[0] if response.json() else None
        # user = UTILISATEUR.query.filter_by(email=session['email'], admin=session['admin']).first()
        if user:
            if session['password'] == user['password']:
                if admin:
                    return user['admin'] == True
                else:
                    return True
    return False