import hashlib
import os
 

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