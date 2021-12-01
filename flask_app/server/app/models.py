from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager
from flask_login import UserMixin

### START OF USER MODEL CODE + AUXILIARY FUNCTIONS ###

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False, index = True)
    password = db.Column(db.String, nullable = False)
    authenticated = db.Column(db.Boolean, default = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object."""
    return User.query.get(user_id)

### END OF USER MODEL CODE ###

### START OF CODE FOR ALL OTHER MODELS ###

class Workouts(db.Model):

    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    setTime = db.Column(db.Integer, nullable=False)
    restTime = db.Column(db.Integer, nullable=False)
    workoutsList = db.Column(db.String(200), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(200), primary_key=True)


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String(200), primary_key=True)
