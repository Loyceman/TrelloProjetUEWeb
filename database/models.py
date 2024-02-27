from flask_login import UserMixin

from database.database import db
import enum
import sqlalchemy


class UserRoleEnum(enum.Enum):
    DEVELOPER = 'Developer'
    PROJECT_MANAGER = 'ProjectManager'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(sqlalchemy.types.Enum(UserRoleEnum), nullable=False)

    def __init__(self, username='', password_hash='', role=''):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
