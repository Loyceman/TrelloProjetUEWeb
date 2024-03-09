import datetime

import flask
from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_login import login_required, logout_user, LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database
from database.models import User, Task, UserRoleEnum, Project, Team
import database.models as models
import os
from helpers import enum_to_readable
from sqlalchemy import inspect

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "this-is-a-secret-key"
db.init_app(app)

with app.test_request_context():
    init_database()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return models.User.query.filter_by(username=user).first()


@app.route('/')
@login_required
def route():
    return redirect('/home_page')


# HOME PAGE
@app.route('/home_page', methods=['POST', 'GET'])
@login_required
def dashboard():
    if request.method == 'POST':
        match request.form['type']:
            case 'project':
                create_project()

    return render_template("home_page.html.jinja2", users=User.query.all())


# HOME PAGE
# Route for retrieving projects
@app.route('/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.all()
    project_data = []
    for project in projects:
        members = [member.username for member in project.members.all()]
        project_data.append({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'color': project.color,
            'endDate': project.endDate,
            'startDate': project.startDate,
            'members': members
        })
    return jsonify(project_data)


def retrieve_data():
    name = request.form['name']
    description = request.form['description']
    color = request.form['color']

    start_date_str = request.form['startDate']
    start_year, start_month, start_day = map(int, start_date_str.split('-'))
    start_date = datetime.date(start_year, start_month,
                               start_day)  # Transforme les dates de javascript en date utilisable par Python

    end_date_str = request.form['endDate']
    end_year, end_month, end_day = map(int, end_date_str.split('-'))
    end_date = datetime.date(end_year, end_month, end_day)

    project_members = request.form.getlist('members[]')  # Récupère une liste des membres du projet

    return name, description, color, start_date, end_date, project_members


# HOME PAGE
def create_project():
    name, description, color, start_date, end_date, members = retrieve_data()
    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        return jsonify({'error': 'A project with the same name already exists'}), 400

    # Création d'un projet et ajout à la base de données
    project = Project(description=description, name=name, color=color, startDate=start_date, endDate=end_date)

    db.session.add(project)

    # Ajout des membres au projet
    for member_name in members:
        member = User.query.filter_by(username=member_name).first()
        if member:
            project.members.append(member)

    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 200


# HOME PAGE
@app.route('/save_project', methods=['POST'])
@login_required
def save_project():
    name, description, color, start_date, end_date, members = retrieve_data()

    # Rechercher le projet existant dans la base de données
    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        # Mettre à jour les champs du projet avec les nouvelles valeurs
        existing_project.description = description
        existing_project.color = color
        existing_project.startDate = start_date
        existing_project.endDate = end_date

        # Supprimer les membres actuels du projet
        for member in existing_project.members:
            db.session.delete(member)

        # Ajouter les nouveaux membres au projet
        for member_id in members:
            member = User.query.get(member_id)
            if member:
                existing_project.members.append(member)

        # Sauvegarder les modifications dans la base de données
        db.session.commit()

        return jsonify({'message': 'Project updated successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404


# PROJECT PAGES
@login_required
@app.route('/projects/standard_view/<int:project_id>', methods=['GET', 'POST'])
def standard_project_page(project_id):
    # Utilisez l'ID du projet pour récupérer les données du projet depuis la base de données
    project = get_project_by_id(project_id)
    return render_template("project_header.html.jinja2", project=project, pid=project_id)


def get_project_by_id(project_id):
    return Project.query.get(project_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # users = User.query.all()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return render_template('login.html.jinja2')
        login_user(user, remember=remember)
        return redirect('/home_page')
    else:
        return render_template('login.html.jinja2')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        user = models.User.query.filter_by(username=username).first()
        if user:
            flash('User already exists')
        elif not username or not password or not role:
            flash('Please fill in all the fields')
        else:
            user = User(username=username,
                        password_hash=generate_password_hash(password, method='sha256'),
                        role=role)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    user_roles_enums = [role.name for role in UserRoleEnum]
    user_roles = [enum_to_readable(role.name) for role in UserRoleEnum]
    return render_template('register.html.jinja2',
                           user_roles_enums=user_roles_enums,
                           user_roles=user_roles,
                           zip=zip)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/database')
def show_database():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    tables = [table for table in tables if not is_junction_table(table)]
    columns_dict = {}
    for table in tables:
        columns = inspector.get_columns(table)
        columns_dict[table] = [column['name'] for column in columns]
    data = {}
    for table in tables:
        model_class = globals()[table.capitalize()]  # Assuming your model class names are capitalized
        data[table] = model_class.query.all()
    return render_template('database.html.jinja2', columns=columns_dict, data=data, getattr=getattr)


def is_junction_table(table_name):
    # You can define your logic to identify junction tables here
    # For example, if a table has only two foreign keys, it's likely a junction table
    # This is a simplified example, you may need to adjust it based on your specific database schema
    inspector = inspect(db.engine)
    foreign_keys = inspector.get_foreign_keys(table_name)
    return len(foreign_keys) == 2


if __name__ == '__main__':
    app.run()
