import os
from flask import Blueprint, request, current_app, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.widgets import TextInput, Input
from wtforms.fields import TextField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from uuid import uuid4
from base64 import urlsafe_b64encode

from . import users, schemes, schemes_pg

class LoginForm(FlaskForm):
    login = TextField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    login = TextField('Логин', validators=[DataRequired()])
    nickname = TextField('Ф.И.О.', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class User(UserMixin):
    def __init__(self, identity, nickname):
        self.identity = identity
        self.nickname = nickname
        self.vendor = None

def get_blueprint():
    auth_bp = Blueprint('auth_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

    login_manager = LoginManager()
    login_manager.init_app(current_app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth_bp.register'))

    @login_manager.user_loader
    def load_user(login):
        conn = users.get_connection()
            
        with conn:
            with conn.cursor() as cursor:
            
                sql = 'select login, identity, nickname from db_jeeves.USER where login = %s'
                cursor.execute(sql, (login))
                sql_id = cursor.fetchone()
                
            if sql_id:
                login, identity, nickname = sql_id.values()

                with conn.cursor() as cursor:
                    sql = 'select db_vendor from db_jeeves.PROJECT where ref_identity = %s'
                    cursor.execute(sql, (identity))
                    sql_rs = cursor.fetchone()
                    vendor = (sql_rs and sql_rs['db_vendor']) or "None"

                mu = User(identity, nickname)
                mu.id = login
                mu.vendor = vendor
                return mu
            
        #session.clear()

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if request.method == 'POST' and form.validate():
            login, password, nickname = form.login.data, form.password.data, form.nickname.data
        
            identity = 'u_' + urlsafe_b64encode(os.urandom(6)).decode().lower()
            
            schemes.create_user(identity)
            schemes_pg.create_user(identity)

            conn = users.get_connection()

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO db_jeeves.USER VALUES(%s, %s, %s, %s)', (login, password, nickname, identity))
                    conn.commit()

                    mu = User(identity, nickname)
                    mu.id = login
                    login_user(mu)
                    
            return redirect(url_for('main'))

        return render_template('register.html', form=form)

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if request.method == 'POST' and form.validate():
            login, password = form.login.data, form.password.data
            conn = users.get_connection()

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT login, identity, nickname FROM db_jeeves.USER where login = %s and password = %s', (login, password))
                    id = cursor.fetchone()
                    if id:
                        mu = User(id['identity'], id['nickname'])
                        mu.id = login
                        login_user(mu)
                        return redirect(url_for('main'))

        return render_template('login.html', form=form)

    @auth_bp.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('.register'))
    
    return auth_bp