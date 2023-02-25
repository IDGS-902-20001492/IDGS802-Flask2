from wtforms import Form 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, IntegerField
from wtforms.fields import EmailField, TextAreaField, PasswordField, RadioField
from wtforms import validators

class dicForm(Form):
    ing = StringField('Ingles',[
        validators.DataRequired(message = 'El campo es requerido')])

    esp = StringField('Español', [
        validators.DataRequired(message = 'El campo es requerido')
    ])

    res = StringField('Resultado:')

class busForm(Form):
    lenguage = RadioField('Buscar', choices=[('es', 'Español'), ('in', 'Inglés')],
                          validators = [validators.InputRequired(message = "El campo es requerido!")])

    busqueda = StringField('Busqueda',[
        validators.DataRequired(message = 'El campo es requerido')
    ])

    
