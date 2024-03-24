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
    LOW_PRIORITY = 'Priorité basse'
    MIDDLE_PRIORITY = 'Priorité moyenne'
    HIGH_PRIORITY = 'Haute priorité'


class TaskCompletionEnum(enum.Enum):
    IN_PROGRESS = 'InProgress'
    DONE = 'Done'
    STUCK = 'Stuck'


class NotifTypeEnum(enum.Enum):
    ASSIGNED = 'ASSIGNED'
    UNASSIGNED = 'UNASSIGNED'
    MODIFIED = 'MODIFIED'


class NotifStatusEnum(enum.Enum):
    READ = True
    NOTREAD = False



# Définir un dictionnaire qui mappe chaque valeur d'énumération avec la classe de badge correspondante
PRIORITY_BADGE_MAPPING = {
    PriorityEnum.LOW_PRIORITY.value: 'badge bg-success',
    PriorityEnum.MIDDLE_PRIORITY.value: 'badge bg-warning',
    PriorityEnum.HIGH_PRIORITY.value: 'badge bg-danger'
}


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
    categories = db.relationship('Category', backref=db.backref('project'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    label = db.Column(sqlalchemy.types.Enum(PriorityEnum), nullable=False)
    description = db.Column(db.Text)
    dueDate = db.Column(db.Date)
    displayable = db.Column(db.Boolean)
    completionStatus = db.Column(sqlalchemy.types.Enum(TaskCompletionEnum), nullable=False)
    users = db.relationship('User', secondary=users_tasks_association,
                            backref=db.backref('tasks'))
    subtasks = db.relationship('Subtask', backref=db.backref('task'))

    def get_project_name(self):
        category = Category.query.get(self.category_id)
        project = Project.query.get(category.project_id)
        if project:
            return project.name
        else:
            return None

    def get_project(self):
        category = Category.query.get(self.category_id)
        project = Project.query.get(category.project_id)
        if project:
            return project
        else:
            return None

    def get_category(self):
        category = Category.query.get(self.category_id)
        if category :
            return category
        else :
            return None

    def get_priority_badge_class(self):
        return PRIORITY_BADGE_MAPPING.get(self.label.value, 'badge bg-secondary')


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    isDone = db.Column(db.Boolean)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def get_task(self):
        task = Task.query.get(self.task_id)
        if task:
            return task
        else:
            return None

class Notif(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    type = db.Column(sqlalchemy.types.Enum(NotifTypeEnum), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(sqlalchemy.types.Enum(NotifStatusEnum), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    tasks = db.relationship('Task', backref=db.backref('category'))

    def get_project(self):
        project = Project.query.get(self.project_id)
        if project :
            return project
        else :
            return None