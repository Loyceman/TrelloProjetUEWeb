import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database
from database.models import User, Task
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.test_request_context():
    init_database()


@app.route('/')
def dashboard():
    # TODO
    user_1 = User(username="Flo", password_hash="oui")
    db.session.add(user_1)
    task_carae = Task(label="Réserver salle CARAE", isDone=False)
    db.session.add(task_carae)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.id, user.username, user.password_hash)
    tasks = Task.query.all()
    for task in tasks:
        print(task.id, task.label, task.isDone)
    return 'Hello World!'


@app.route('/project/<project_id>')
@login_required
def project(project_id):
    # TODO
    return 'Project ' + project_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO
        return redirect('/')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    # TODO
    return redirect('/')


if __name__ == '__main__':
    app.run()
