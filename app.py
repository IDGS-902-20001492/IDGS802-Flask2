from flask import Flask,render_template
from flask import request
from collections import Counter
from flask_wtf import FlaskForm
from wtforms import validators
from flask_wtf.csrf import CSRFProtect 
from flask import make_response
from flask import flash
import forms
import cajas
import diccionario

app = Flask(__name__)
app.config['SECRET_KEY'] = "Esta es mi clave encriptada"
csrf = CSRFProtect()


@app.route("/formulario2",methods = ["GET"])
def formulario2():
    return render_template("formulario2.html")

@app.errorhandler(404)
def no_encontrada(e):
    return render_template("404.html"),404

@app.before_request
def before_request():
    print("numero1")


@app.route("/cookies", methods = ["GET","POST"])
def cookies():
    print("numero2")
    reg_user = forms.LoginForm(request.form)
    response = make_response(render_template('cookies.html',form = reg_user))
    if request.method == 'POST' and reg_user.validate():
        user = reg_user.username.data
        pasw = reg_user.password.data
        datos = user+'@'+pasw
        success_message = 'Bienvenido {}'.format(user)
        flash(success_message)
        response.set_cookie('datos_user',datos)
        
    return response

@app.after_request
def after_request(response):
    print("numero3")
    return response
    
@app.route("/saludo")
def saludo():
    valor_cookie = request.cookies.get('datos_user')
    nombre = valor_cookie.split('@')
    return render_template('saludo.html',nom = nombre[0])    

@app.route("/Alumnos",methods = ["GET","POST"])
def alumno():
        alum_form = forms.UserForm(request.form)
        mat = ''
        nom = ''
        if request.method == 'POST' and alum_form.validate():    
            print(alum_form.matricula.data)
            print(alum_form.nombre.data)
            #alum_form.form.apeP.data
            #alum_form.form.apeM.datacm
            #alum_form.form.email.data
        return render_template("Alumnos.html", form=alum_form, mat = alum_form.matricula,
         nom = alum_form.nombre)

@app.route("/CajasD",methods = ["GET","POST"])
def box():
        formC = cajas.Cajas(request.form)

        if request.method == 'POST': 
            print(formC.nCajas.data)

            btn = request.form.get("btn")
            if btn == 'Cargar':
                return render_template('cajasD.html',form=formC)
            
            if btn == 'Datos':
                numero = request.form.getlist("numeros")
                max_value = None
                for num in numero:
                    num = int(num)
                    if (max_value is None or num > max_value):
                        
                        max_value = num

                min_value = None
                for num in numero:
                    num = int(num)
                    if (min_value is None or num <= min_value):
                        
                        min_value = num

                for i in range(len(numero)):
                    numero[i] = int(numero[i])


                prom = 0
                prom = sum(numero) / len(numero)

                counter = Counter(numero)
                resultados = counter.most_common()
                txtRes = ''

                for r in resultados:
                    if r[1] > 1:
                        txtRes += '<p>El número {0} se repite {1} veces</p>'.format(r[0], r[1])
            
                return render_template('cajasRes.html',form=formC, max_value=max_value, min_value=min_value, prom=prom, repetidos = txtRes)
        return render_template("cajasD.html", form = formC)

@app.route("/dic",methods = ["GET","POST"])
def dicc():
        dForm = diccionario.dicForm(request.form) 
        bForm = diccionario.busForm(request.form) 
        
        textoE = dForm.esp.data
        textoI = dForm.ing.data
        busc = bForm.busqueda.data
        idioma = bForm.lenguage.data

        textoE = str(textoE).lower()
        textoI = str(textoI).lower()
        busc =str(busc).lower()


        btn = request.form.get('btn')

        if request.method == 'POST':

            if btn == 'Guardar' and dForm.validate():
             
             trad = open('traduccion.txt','a')
             trad.write("\n"+textoE+"\n"+textoI)
             
             trad.close()

            if btn == 'Buscar' and bForm.validate():             
             if idioma == 'in':
                traduccion = ""
                i = 0

                with open('traduccion.txt', 'r') as archivo:
                 contenido = archivo.read()

                palabras = contenido.split('\n')  
                for coincidencia in palabras:
                    if busc in coincidencia.lower():
                        traduccion = palabras[i+1]
                    
                    i = i+1



                return render_template("diccionario.html",bform = bForm,dform = dForm, resultado = traduccion)

             else:

                traduccion = ""
                i = 0
                with open('traduccion.txt', 'r') as archivo:
                 contenido = archivo.read()

                palabras = contenido.split('\n')  
                for coincidencia in palabras:
                    if busc in coincidencia:
                        traduccion = palabras[i-1]
                   
                    i = i+1
                return render_template("diccionario.html",bform = bForm,dform = dForm, resultado = traduccion)

        return render_template("diccionario.html",dform = dForm, bform = bForm)



if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug = True, port = 3000)