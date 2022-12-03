import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
#from flask_socketio import SocketIO, join_room, leave_room, send
from wtform_fields import *
from models import *
from passlib.hash import pbkdf2_sha256

# Configuração do aplicativo
app = Flask(__name__)
app.secret_key = "esperar"
# app.secret_key = os.environ.get('SECRET')
# app.config['WTF_CSRF_SECRET_KEY'] = "esperar"

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lliyjhsrrdfcxi:99b702fdf65fb70cc709dd07decd7a29a1ec9f3af0047ad59008f7b9f3989a1b@ec2-3-229-252-6.compute-1.amazonaws.com:5432/d1lqcbskn156vq'
db = SQLAlchemy(app)

# Configuração flask login
login = LoginManager(app)
login.init_app(app)

# Parâmetros de listas atualizações para o sistema
lista_grod = ['CARLOS MOUSINHO', 'DANIELE MALFACINI', 'EDUARDO JULIO', 'FLAVIO ITO', 'MARIANA PESENTI', 'PEDRO FOLEGOTTO', 'RODRIGO BASILIO', 'EDSON BARRETO', 'JOAO NETO']
lista_rod = ['ANDRE MENDONCA', 'ARTHUR VIEIRA', 'CAMILLA BERNARDES', 'EDNISE SANTOS', 'EDUARDO FERNANDES', 'ERVEN NETO', 'FERNANDO MENDONCA', 'FLAVIO DIAS', 'GIOVANA CARVALHO', 'ISIS FERREIRA', 'LEANDRO SILVA', 'LUCILENE PIRES', 'MARCELO OTA', 'MARIA LEITE', 'MARIANNE ASSBU', 'NYANZA LIMA', 'RENATA ANDRADE', 'ROMERIO SALES', 'SONIA PINHEIRO', 'TEOLANDIA DUARTE']
lista_operacao = []

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

# class Novidade(db.Model):
    # __tablename__ = 'novidade'
    # id = db.Column(db.Integer, primary_key=True)
    # e_mail_info = db.Column(db.String(200), unique=True)

    # def __init__(self, e_mail_info):
        #self.e_mail_info = e_mail_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        e_mail_info = request.form['emailAddress']
        print(e_mail_info)
        return render_template('success.html')

@app.route('/register', methods=['GET', 'POST'])
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

    return render_template('register.html', form=reg_form)

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

#Vou colocar aqui cada processo
#id:P0001_DIR000_C0000
@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao():
    return render_template('movimentacao.html', lista_grod=lista_grod, lista_rod=lista_rod, lista_operacao=lista_operacao)


# Código Final para Rodar o Site
if __name__ == '__main__':
    app.run(debug=True)

    