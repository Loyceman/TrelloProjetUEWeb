from flask_login import UserMixin

import enum
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy

db = SQLAlchemy()

users_projects_association = db.Table('user_project_associations',
                                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                      db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
                                      )

users_tasks_association = db.Table('user_tasks_associations',
                                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                   db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                                   )


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
        return self.username


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    color = db.Column(db.String(7))  # Stocke la couleur au format hexadécimal
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    users = db.relationship('User', secondary=users_projects_association,
                            backref=db.backref('projects'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    dueDate = db.Column(db.Date)
    isDone = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    users = db.relationship('User', secondary=users_tasks_association,
                            backref=db.backref('tasks'))
