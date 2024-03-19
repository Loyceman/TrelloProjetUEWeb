import datetime
from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_login import login_required, logout_user, LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database, get_relationship_names
from database.models import UserRoleEnum, User, Task, Project, Notif, Subtask
import database.models as models
import os
from helpers import enum_to_readable
from sqlalchemy import inspect

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "this-is-a-secret-key"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
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
    return render_template("home_page.html.jinja2", users=User.query.all())


# HOME PAGE
# Route for retrieving projects
@app.route('/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.all()
    project_data = []
    for project in projects:
        members_id = [user.id for user in project.users]
        members = []
        for member_id in members_id:
            members.append(User.query.get(member_id).username)
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
    start_date = datetime.date.today()
    end_date = datetime.date(2024, 12, 30)

    if request.form['startDate']:
        start_date_str = request.form['startDate']
        start_year, start_month, start_day = map(int, start_date_str.split('-'))
        start_date = datetime.date(start_year, start_month,
                                   start_day)  # Transforme les dates de javascript en date utilisable par Python
    if request.form['endDate']:
        end_date_str = request.form['endDate']
        end_year, end_month, end_day = map(int, end_date_str.split('-'))
        end_date = datetime.date(end_year, end_month, end_day)

    project_members = request.form.getlist('members[]')  # Récupère une liste des membres du projet

    return name, description, color, start_date, end_date, project_members


# HOME PAGE
@app.route('/create_project', methods=['POST'])
@login_required
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
            project.users.append(member)

    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 200


# HOME PAGE
@app.route('/delete_project', methods=['POST'])
@login_required
def delete_project():
    id_project = request.form['id']
    project = Project.query.filter_by(id=id_project).first()
    if project:
        db.session.delete(project)
        db.session.commit()  # Confirmer la suppression
        return jsonify({'message': 'Project deleted successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404


# HOME PAGE
@app.route('/save_project', methods=['POST'])
@login_required
def save_project():

    print("\n==== SAVING PROJECT ====\n")
    name, description, color, start_date, end_date, members = retrieve_data()

    # Rechercher le projet existant dans la base de données
    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        # Mettre à jour les champs du projet avec les nouvelles valeurs
        existing_project.description = description
        existing_project.color = color
        existing_project.startDate = start_date
        existing_project.endDate = end_date
        print("    Current Project : " + str(existing_project))
        print("        Description : " + description)
        print("        Color : " + str(color))
        print("        Start Date : " + str(start_date))
        print("        End Date : " + str(end_date))
        print("        Members : " + str(members))
        # Supprimer les membres actuels du projet
        for member in existing_project.users:
            existing_project.users.remove(member)
        print("\n    Deleted previous members from project")


        # Ajouter les nouveaux membres au projet
        print("    Adding new members :")
        for member_name in members:
            member = User.query.filter_by(username=member_name).first()
            if member:
                existing_project.users.append(member)
                print("        Added user " + member.username)

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
    return render_template("project_standard_view.html.jinja2", project=project, pid=project_id)


def get_project_by_id(project_id):
    return Project.query.get(project_id)


@login_required
@app.route('/current_user', methods=['GET'])
def get_current_user():
    user_projects = current_user.get_project()
    projects_data = [{"id": project.id, "name": project.name} for project in user_projects]
    if current_user.is_authenticated:
        user_details = {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role.value,
            "projects": projects_data
        }
        return jsonify(user_details)
    else:
        return jsonify({"error": "No users are currently logged in"}), 401


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("==== LOGIN PAGE ====\n")
    users = User.query.all()
    print("    Users in the database :")
    for user in users:
        print("         ID: {:<3}  | Username: {:<15}  | Password: {:<100}".format(user.id, user.username,
                                                                                   user.password_hash))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(username=username).first()
        print("Username : ", username)
        print("Password : ", password)
        print("Remember : ", remember)
        print(check_password_hash(user.password_hash, password))
        print(generate_password_hash(password))
        print(user.password_hash)
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
    print("\n==== SHOWING THE DATABASE ====\n")
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    tables = [table for table in tables if not is_junction_table(table)]
    columns_dict = {}
    for table in tables:
        columns = inspector.get_columns(table)
        columns_dict[table] = [column['name'] for column in columns]
    data = {}
    print("    Structure :")
    print("        Tables : ", tables)
    print("        Columns : ")
    for table, columns in columns_dict.items():
        print("            " + table + " : " + str(columns))
    print("\n    Data :")
    for table in tables:
        print("        " + table.capitalize() + " :")
        model_class = globals()[table.capitalize()]
        data[table] = model_class.query.all()
        print("            Instances :" + str(data[table]))

        relationships = get_relationship_names(model_class)
        if not relationships:
            continue
        print("            Relationships with classes :", get_relationship_names(model_class))

        for instance in data[table]:
            print("            Instance :", instance)
            for relationship in relationships:
                print("                Linked with instances of class " + relationship, end="")
                linked_objects = getattr(instance, relationship)
                if hasattr(linked_objects, "__iter__"):
                    linked_ids = [linked_object.id for linked_object in linked_objects]
                else :
                    linked_ids = linked_objects.id
                print(" with ids : " + str(linked_ids))

    return render_template('database.html.jinja2', columns=columns_dict, data=data, getattr=getattr)


def is_junction_table(table_name):
    inspector = inspect(db.engine)
    foreign_keys = inspector.get_foreign_keys(table_name)
    columns = inspector.get_columns(table_name)
    return len(foreign_keys) == 2 and len(columns) == 2


if __name__ == '__main__':
    app.run()
