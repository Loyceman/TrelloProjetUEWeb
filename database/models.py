from flask_login import UserMixin

import enum
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy

db = SQLAlchemy()


# Table de liaison pour la relation Many-to-Many
users_projects_association = db.Table('project_members', db.Model.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                           )
users_tasks_association = db.Table('task_members', db.Model.metadata,
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True))


class UserRoleEnum(enum.Enum):
    DEVELOPER = 'Developer'
    PROJECT_MANAGER = 'ProjectManager'


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(sqlalchemy.types.Enum(UserRoleEnum), nullable=False)

    projects = db.relationship('Project', secondary=users_projects_association, backref="User")
    tasks = db.relationship("Task", secondary=users_tasks_association, backref="User")

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
    endDate = db.Column(db.DateTime)
    startDate = db.Column(db.DateTime)
    # Relation Many-to-Many avec la table project_members
    members = db.relationship('User',
                              secondary=project_members,
                              backref=db.backref('projects', lazy='dynamic'),
                              lazy='dynamic')


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    dueDate = db.Column(db.Date)
    isDone = db.Column(db.Boolean)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    users = db.relationship('User', secondary=users_tasks_association, backref='Task')