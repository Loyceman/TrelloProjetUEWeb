import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import db, init_database
from database.models import User

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


user_1 = User(username="Flo", password_hash="oui")
db.session.add(user_1)
db.commit()
print(User.query.all)

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
