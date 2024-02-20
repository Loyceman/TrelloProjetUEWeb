import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

app = Flask(__name__)


@app.route('/')
def dashboard():
    # TODO
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
    else :
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO
        return redirect('/')
    else :
        return render_template('register.html')


@app.route('/logout')
def logout():
    # TODO
    return redirect('/')


if __name__ == '__main__':
    app.run()
