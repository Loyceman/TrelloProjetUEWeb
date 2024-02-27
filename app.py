import flask
from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database
from database.models import User, Task, UserRoleEnum
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


@app.route('/home_page', methods=['GET', 'POST'])
@login_required
def dashboard():
    # if not current_user.is_authenticated :
    #     redirect('/login')
    # else:
    return render_template("home_page.html.jinja2")


def create_project():
    name = request.form.get('name')
    description = request.form.get('description')

    # Create project and add it to the database
    project = models.Project(id=0, description=description)
    db.session.add(project)
    db.session.commit()


# Route for retrieving projects
def get_projects():
    projects = models.Project.query.all()
    project_data = [{'name': project.name, 'description': project.description} for project in projects]
    return jsonify(project_data)

def create_project():
    name = request.form['name']
    description = request.form['description']

    # Create project and add it to the database
    project = Project(description=description, name=name)
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 200


# Route for retrieving projects
# def get_projects():
#    projects = Project.query.all()
#    print(projects)
#    project_data = [{'name': project.name, 'description': project.description} for project in projects]
#    print(project_data)
#    return jsonify(project_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Users :")
    users = User.query.all()
    for user in users:
        print(user.id, user.username, user.password_hash)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(username=username).first()
        print("Username : ", username)
        print("Password : ", password)
        print("Remember : ", remember)
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return render_template('login.html.jinja2')
        login_user(user, remember=remember)
        print("User logged in")
        return redirect('/')
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
    return redirect('/')


@app.route('/database')
def show_database():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    columns_dict = {}
    for table in tables:
        columns = inspector.get_columns(table)
        columns_dict[table] = [column['name'] for column in columns]
    data = {}
    for table in tables:
        model_class = globals()[table.capitalize()]  # Assuming your model class names are capitalized
        data[table] = model_class.query.all()
    return render_template('database.html.jinja2', columns=columns_dict, data=data, getattr=getattr)


if __name__ == '__main__':
    app.run()
