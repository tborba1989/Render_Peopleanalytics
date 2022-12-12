import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send
from wtform_fields import *
from models import *
from passlib.hash import pbkdf2_sha256
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Configuração do aplicativo
app = Flask(__name__)
app.secret_key = 'test'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:5TGDWnQvo6nZDIXJszGxhpItXk5HGMay@dpg-ce5pqpla4991uet9rohg-a.ohio-postgres.render.com/peopleanalytics'
db = SQLAlchemy(app)

# Configuração flask login
login = LoginManager(app)
login.init_app(app)

# Parâmetros de listas atualizações para o sistema
lst_0 = ['teste1', 'teste2', 'teste3']
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        e_mail_info = request.form['emailAddress']
        print(e_mail_info)
        return render_template('success.html')
@app.route('/inscricao', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    # atualiza banco se a validação da credencial for sucesso
    if reg_form.validate_on_submit():
        usuario = reg_form.usuario.data
        nome = reg_form.nome.data
        telefone = reg_form.telefone.data
        emailcorp = reg_form.emailcorp.data
        senha = reg_form.senha.data

        # senha criptografada
        hashed_senha = pbkdf2_sha256.hash(senha)

        # adiciona novo usuário
        usr = User(usuario=usuario, nome=nome, telefone=telefone, emailcorp=emailcorp, senha=hashed_senha)
        db.session.add(usr)
        db.session.commit()

        flash('Registro efetuado com sucesso. Faça o login.', 'success')

        return redirect(url_for('login'))

    return render_template('inscricao.html', form=reg_form)
@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # permite o usuario realizar a entrada no sistema
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(usuario=login_form.usuario.data).first()
        login_user(user_object)
        return redirect(url_for('dashboard'))

    return render_template('login.html', form=login_form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if not current_user.is_authenticated:
        flash('Por favor, realize o login.', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html')
@app.route('/logout', methods=['GET'])
def logout():
    # se não estiver autenticado
    logout_user()
    flash('Você fez Logout através da Sessão!', 'success')
    return redirect(url_for('index'))

@app.route('/exemplo', methods=['GET', 'POST'])
def exemplo():
    return render_template('exemplo.html')

# Código Final para Rodar o Site
if __name__ == '__main__':
    app.run(debug=True)
