import os

def test_connection(user):
    if os.getenv('AUTH_USERNAME') == user.username and os.getenv('AUTH_PASSWORD') == user.password:
        return True
    return False