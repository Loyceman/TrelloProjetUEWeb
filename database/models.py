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

users_notifs_association = db.Table('user_notifs_associations',
                                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                    db.Column('notif_id', db.Integer, db.ForeignKey('notif.id'))
                                    )


class UserRoleEnum(enum.Enum):
    DEVELOPER = 'Developer'
    PROJECT_MANAGER = 'ProjectManager'


class PriorityEnum(enum.Enum):
    LOW_PRIORITY = 'Low priority'
    MIDDLE_PRIORITY = 'Middle priority'
    HIGH_PRIORITY = 'High priority'


class TaskCompletionEnum(enum.Enum):
    IN_PROGRESS = 'InProgress'
    DONE = 'Done'
    STUCK = 'Stuck'


class NotifTypeEnum(enum.Enum):
    ASSIGNED = 'Assigned'
    MODIFIED = 'Modified'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(sqlalchemy.types.Enum(UserRoleEnum), nullable=False)

    # Relation Many-to-Many avec la table project_members
    # members = db.relationship('Project', secondary=project_members,
    #                           backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username='', password_hash='', role=''):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def get_project(self):
        return self.projects

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
    tasks = db.relationship('Task', backref=db.backref('project'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text)
    label = db.Column(sqlalchemy.types.Enum(PriorityEnum), nullable=False)
    description = db.Column(db.Text)
    dueDate = db.Column(db.Date)
    completionStatus = db.Column(sqlalchemy.types.Enum(TaskCompletionEnum), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    users = db.relationship('User', secondary=users_tasks_association,
                            backref=db.backref('tasks'))
    subtasks = db.relationship('Subtask', backref=db.backref('task'))


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Notif(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    type = db.Column(sqlalchemy.types.Enum(NotifTypeEnum))
    users = db.relationship('User', secondary=users_notifs_association,
                            backref=db.backref('notifs'))
