from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *
from passlib.hash import pbkdf2_sha256

def invalid_credentials(form, field):
    """ Checagem de Usuario e senha  """

    usuario_informado = form.usuario.data
    senha_informada = field.data

    # checar se o usuário é valido
    usuario_object = User.query.filter_by(usuario=usuario_informado).first()
    if usuario_object is None:
        raise ValidationError("Usuário ou senha incorretos.")
    elif not pbkdf2_sha256.verify(senha_informada, usuario_object.senha):
        raise ValidationError("Usuário ou senha incorretos.")

class RegistrationForm(FlaskForm):
    """ Registration form"""

    usuario = StringField('usuario_label', validators=[InputRequired(message="Necessário escolher um nome de usuário."), Length(min=5, max=25, message="Nome do Usuário deverá ter entre 5 e 25 caracteres")], render_kw={"placeholder": "Usuario"})
    nome = StringField('nome_label', validators=[InputRequired(message="Necessário seu nome completo."), Length(min=3, max=100, message="Nome do Usuário deverá ter entre 3 e 100 caracteres")], render_kw={"placeholder": "Nome"})
    telefone = StringField('telefone_label', validators=[InputRequired(message="Necessário infomar um Telefone."), Length(min=15, max=15, message="O telefone deverá conter 15 caracteres (xx) xxxxx-xxxx.")], render_kw={"placeholder": "Telefone"})
    emailcorp = StringField('emailcorp_label', validators=[InputRequired(message="Necessário infomar o E-mail de contato."), Length(min=5, max=50, message="Poderá ser qualquer e-mail de contato.")], render_kw={"placeholder": "Emailcorp"})
    senha = PasswordField('senha_label', validators=[InputRequired(message="Necessário infomar uma senha."), Length(min=8, max=50, message="A deverá ter entre 8 e 12 caracteres. 1 Letra maiúscula; 1 Letra minúscula, 1 char. especial, 1 número")], render_kw={"placeholder": "Senha"})
    confirma_senha = PasswordField('confirma_senha_label', validators=[InputRequired(message="Confirmação de senha necessária."), EqualTo('senha', message="As senhas devem ser iguais.")])
    confirma = SubmitField('Criar Conta')

    def validate_usuario(self, usuario):
        usuario_object = User.query.filter_by(usuario=usuario.data).first()
        if usuario_object:
            raise ValidationError("Este usuário já foi escolhido. Escolha um usuário diferente.")

class LoginForm(FlaskForm):
    """ Login form"""

    usuario = StringField('usuario_label', validators=[InputRequired(message="Necessário informar o nome de usuário.")])
    senha = PasswordField('senha_label', validators=[InputRequired(message="Necessário infomar a senha."), invalid_credentials])
    confirma = SubmitField('Entrar')

