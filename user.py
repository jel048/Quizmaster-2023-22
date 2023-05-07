from UserRegister import UserReg
from werkzeug.security import generate_password_hash, check_password_hash


class User():

    # construct / attributes
    def __init__(self, id,username, passwordHash, isAdmin):
        self.id = id
        self.username = username
        self.passwordHash = passwordHash.replace("\'", "")
        self.isAdmin = isAdmin
        self.is_authenticated = True
        self.is_active= True
        self.is_anonymous = False


    @staticmethod
    def login(username, password):

        with UserReg() as db:
            usr = db.getUser(username)
            if usr:
                user = User(*usr)
                pwd = user.passwordHash.replace("\'", "")
                if check_password_hash(pwd, password):
                    return True
            return False

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def __str__(self):
        return f'Id: {self.id}\n' + \
               f'Username: {self.username}\n' + \
               f'Password Hash: {self.passwordHash}'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get(self,id):
        with UserReg() as db:
            user = User(*db.getUserById(id))
            if user:
                return user
            else:
                return False