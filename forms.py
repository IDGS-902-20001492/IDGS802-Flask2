from wtforms import Form 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, IntegerField
from wtforms.fields import EmailField, TextAreaField, PasswordField
from wtforms import validators

def mi_validacion(Form, field):
    if len(field.data) == 0:
        raise validators.ValidationError('EL campo no tiene datos')

class UserForm(Form):
    matricula = StringField('Matricula',[
        validators.DataRequired(message = 'La matricula es requerida')])

    nombre = StringField('Nombre', [
        validators.DataRequired(message = 'La campo es requerido'),
        validators.length(min=5, max=15, message='Ingresa un valor maximo')
    ])
    apeP = StringField('Apellido Paterno', [mi_validacion])
    apeM = StringField('Apellido Materno')
    email = EmailField('Email')

class LoginForm(Form):
    username = StringField('Usuario',[
        validators.DataRequired(message = 'El usuario es requerido')])

    password = PasswordField('Contraseña', [
        validators.DataRequired(message = 'La campo es obligatorio'),
        validators.length(min=5, max=15, message='Ingresa un valor maximo')
    ])
