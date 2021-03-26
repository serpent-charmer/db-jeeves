import os
from flask import Blueprint, request, current_app, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.widgets import TextInput, Input
from wtforms.fields import TextField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from uuid import uuid4
from base64 import urlsafe_b64encode

from . import users, schemes

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

def get_blueprint():
    auth_bp = Blueprint('register_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

    login_manager = LoginManager()
    login_manager.init_app(current_app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect('/register')

    @login_manager.user_loader
    def load_user(login):
        conn = users.get_connection()
            
        with conn:
            with conn.cursor() as cursor:
            
                sql = 'select login, identity, nickname from db_jeeves.USER where login = %s'
                cursor.execute(sql, (login))
                id = cursor.fetchone()
                
        
        if id:
            mu = User(id['identity'], id['nickname'])
            mu.id = id['login']
            return mu
            
        #session.clear()

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if request.method == 'POST' and form.validate():
            login, password, nickname = form.login.data, form.password.data, form.nickname.data
        
            identity = "new-user-"+urlsafe_b64encode(os.urandom(6)).decode().lower()

            conn = users.get_connection()

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO db_jeeves.USER VALUES(%s, %s, %s, %s)', (login, password, nickname, identity))
                    conn.commit()

                    mu = User(identity, nickname)
                    mu.id = login
                    login_user(mu)

            dname = 'database-{}'.format(identity)
            schema_sql = '''
            START TRANSACTION;
            CREATE USER '{0}' IDENTIFIED WITH mysql_native_password BY 'abc';
            CREATE DATABASE `{1}`;
            GRANT ALL PRIVILEGES ON `{1}` . * TO '{0}';
            FLUSH PRIVILEGES;
            COMMIT;
            '''.format(identity, dname)

            conn = schemes.get_root_connection()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(schema_sql)
                    conn.commit()
                    
            return redirect('/')

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
                        return redirect('/')

        return render_template('login.html', form=form)

    @auth_bp.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect('/')
    
    return auth_bp