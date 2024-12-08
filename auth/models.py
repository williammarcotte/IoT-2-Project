from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# sample user using bcrypt to hash password
users = {
    "admin": User(id=1, username="admin", password_hash=bcrypt.generate_password_hash("password").decode('utf-8'))
}

def get_user(username):
    return users.get(username)
