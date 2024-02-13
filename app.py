import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
