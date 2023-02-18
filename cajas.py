from wtforms import Form 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, IntegerField
from wtforms.fields import EmailField, TextAreaField, PasswordField
from wtforms import validators

class Cajas(Form):
    nCajas = IntegerField('Introduzca el número de contenedores')
    numero = FieldList(StringField('numero'), min_entries=1)