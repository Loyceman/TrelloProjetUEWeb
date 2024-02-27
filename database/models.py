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
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    isDone = db.Column(db.Boolean)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)


junction_table = db.Table('team by project',
                          db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
                          db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
                          )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
