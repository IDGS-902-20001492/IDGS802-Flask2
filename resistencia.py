from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, IntegerField
from wtforms.fields import EmailField, TextAreaField, PasswordField,RadioField
from wtforms import validators,Form


class resisCampos(Form):
    opciones = [('','Seleccione una opción'),('0', 'Negro'), ('1', 'Café'), ('2', 'Rojo'),
                ('3', 'Naranja'), ('4', 'Amarillo'), ('5', 'Verde'),
                ('6', 'Azúl'), ('7', 'Violeta'), ('8', 'Gris'),('9','Blanco')]

    opMulti = [('','Seleccione una opción'),('1.0', 'Negro'), ('10', 'Café'), ('100', 'Rojo'),
                ('1000', 'Naranja'), ('10000', 'Amarillo'), ('100000', 'Verde'),
                ('1000000', 'Azúl'), ('10000000', 'Violeta'), ('100000000', 'Gris'),('1000000000','Blanco'),
                ('00.1','Dorado'),('00.01','Plateado'),('nin','Ninguno')]

    banda1 = SelectField('Banda 1: ', choices = opciones,
                          validators = [validators.DataRequired(message = "¡El campo es requerido!")])

    banda2 = SelectField('Banda 2: ', choices = opciones,
                          validators = [validators.DataRequired(message = "¡El campo es requerido!")])
    
    banda3 = SelectField('Banda 3 (Multiplicador): ', choices = opMulti,
                          validators = [validators.DataRequired(message = "¡El campo es requerido!")])

    banda4 = RadioField('Banda 4 (Tolerancia): ', choices=[('0.05', 'Dorado'), ('0.1', 'Plata')],
                        validators = [validators.InputRequired(message = "El campo es requerido!")])
    
