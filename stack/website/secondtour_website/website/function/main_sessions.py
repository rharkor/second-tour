def save_user(session, user):
    session['email'] = user["email"]
    session['password'] = user["password"]
    session['admin'] = user["admin"]
    session.permanent = True

def delete_user(session):
    session.pop('email', default=None)
    session.pop('password', default=None)
    session.pop('admin', default=None)
