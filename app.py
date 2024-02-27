import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database
from database.models import User, Task, UserRoleEnum
import database.models as models
import os
from helpers import enum_to_readable

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
def dashboard():
    return render_template("index.html.jinja2")


@app.route('/project/<project_id>')
@login_required
def project(project_id):
    # TODO
    return 'Project ' + project_id


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
            return render_template('register.html.jinja2')
        print("Username : ", username)
        print("Password : ", password)
        if username and password and role:
            user = User(username=username,
                        password_hash=generate_password_hash(password, method='sha256'),
                        role=role)
            db.session.add(user)
            db.session.commit()
        else:
            return "Please fill all the fields"
        return redirect('/login')
    else:
        user_roles_enums = [role.name for role in UserRoleEnum]
        user_roles = [enum_to_readable(role.name) for role in UserRoleEnum]
        return render_template('register.html.jinja2', user_roles_enums=user_roles_enums, user_roles=user_roles, zip=zip)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/database')
def show_database():
    users_list = User.query.all()
    tasks_list = Task.query.all()
    return render_template('database.html.jinja2', users_list=users_list, tasks_list=tasks_list)


if __name__ == '__main__':
    app.run()

