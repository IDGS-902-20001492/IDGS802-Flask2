from flask import Flask,render_template
from flask import request, redirect
from collections import Counter
from flask_wtf import FlaskForm
from wtforms import validators
from flask_wtf.csrf import CSRFProtect 
from flask import make_response
from flask import flash
from django.shortcuts import render
from django.utils.safestring import mark_safe
import forms
import cajas
import diccionario
import resistencia

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
    #print("numero2")
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
  #  print("numero3")
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
                    if busc == coincidencia.lower():                        
                        traduccion = palabras[i+1]
                    if traduccion == '':
                        traduccion = 'La palabra no existe'
                    i = i+1



                return render_template("diccionario.html",bform = bForm,dform = dForm, resultado = traduccion)

             else:

                traduccion = ""
                x = 0
                with open('traduccion.txt', 'r') as archivo:
                 contenido = archivo.read()
                print("Ingles a español")
                palabras = contenido.split('\n')  
                print(palabras)
                for coincidencia in palabras:
                    
                    if busc == coincidencia.lower():                        
                        traduccion = palabras[x-1]
                        print(coincidencia)
                    if traduccion == '':
                        traduccion = 'La palabra no existe'                                               
                    x = x+1

             return render_template("diccionario.html",bform = bForm,dform = dForm, resultado = traduccion)

        return render_template("diccionario.html",dform = dForm, bform = bForm)

@app.route("/resistencia",methods = ["GET","POST"])
def resistencias():
        
        resisForm = resistencia.resisCampos(request.form)
        btn = request.form.get('btn')
        
        encabezado = request.cookies.get('encabezado')
        cuerpo = request.cookies.get('cuerpo')
                                           
        b1 = ""
        b2 = ""
        b3 = ""
        b4 = ""
        thead = ""
        tbody = ""
        valor = 0
        min = 0
        max = 0
        elementos = []

        color = ""
        
        if request.method == 'POST' and resisForm.validate():
            
            if btn == 'Calcular':
                response = make_response(render_template('resistencias.html',form = resisForm,
                           thead = mark_safe(encabezado),
                                                 tbody = mark_safe(cuerpo)))
                response.delete_cookie('encabezado')
                response.delete_cookie('cuerpo')
                

                b1 = resisForm.banda1.data
                b2 = resisForm.banda2.data
                b3 = resisForm.banda3.data
                b4 = resisForm.banda4.data

                if b3 == 'nin':
                    b3 = '1'

                banda12 = str(b1)+str(b2)+""
                valor = float(banda12)*float(b3)

                if b4 == "0.05":
                    min = valor - valor*0.05
                    max = valor + valor*0.05
                else:
                    min = valor - valor*0.1
                    max = valor + valor*0.1    

                if b3 == "nin":
                    min = valor - valor*.2
                    max = valor + valor*.2

                elementos = [b1, b2, b3, b4, valor, min, max]
            
                thead = "<style>th{border:2px solid black;}</style><th>Banda1</th><th>Banda2</th><th>Banda3</th><th>Banda4</th><th>Valor(Ohms)</th><th>Minimo</th><th>Maximo</th>"
                tbody = "<style>td{border:2px solid black;}</style><tr>"
                for temp in elementos:
                    if temp == '0' or temp == '1.0':
                        color = '#000000'
                        tbody += "<td style='background-color: "+color+";'><a style='color:white;'>"+"negro"+"</a></td>"
                    elif temp == '1' or temp == '10':
                        color = '#6e5b53'
                        tbody += "<td style='background-color: "+color+";'>"+"cafe"+"</td>"
                    elif temp == '2' or temp == '100':
                        color = '#e71837'
                        tbody += "<td style='background-color: "+color+";'>"+"rojo"+"</td>"
                    elif temp == '3' or temp == '1000':
                        color = '#fc9303'
                        tbody += "<td style='background-color: "+color+";'>"+"naranja"+"</td>"
                    elif temp == '4' or temp == '10000':
                        color = '#fce903'
                        tbody += "<td style='background-color: "+color+";'>"+"amarillo"+"</td>"
                    elif temp == '5' or temp == '100000':
                        color = '#49b675'
                        tbody += "<td style='background-color: "+color+";'>"+"verde"+"</td>"
                    elif temp == '6' or temp == '1000000':
                        color = '#0e4bef'
                        tbody += "<td style='background-color: "+color+";'>"+"azul"+"</td>"
                    elif temp == '7' or temp == '10000000':
                        color = '#c71585'
                        tbody += "<td style='background-color: "+color+";'>"+"violeta"+"</td>"
                    elif temp == '8' or temp == '100000000':
                        color = '#868686' 
                        tbody += "<td style='background-color: "+color+";'>"+"gris"+"</td>"
                    elif temp == '9' or temp == '1000000000':
                        color = '#ffffff'
                        tbody += "<td style='background-color: "+color+";'>"+"blanco"+"</td>"
                    elif temp == '0.05' or temp == '00.1':
                        color = '#cccc33'  
                        tbody += "<td style='background-color: "+color+";'>"+"dorado"+"</td>"
                    elif temp == '0.1' or temp == '00.01':
                        color = '#bfc1c1' 
                        tbody += "<td style='background-color: "+color+";'>"+"plateado"+"</td>"                                          
                    else:
                        tbody += "<td>"+str(temp)+"</td>"

                tbody += "</tr>"
                thead = mark_safe(thead)
                tbody = mark_safe(tbody)

                
                flash("El valor resultante es: "+str(valor))                

                response.set_cookie('encabezado',thead)
                response.set_cookie('cuerpo',tbody)
                print(thead+tbody)
        else:
            response = make_response(render_template('resistencias.html',form = resisForm,
                           thead = mark_safe(encabezado),
                                                 tbody = mark_safe(cuerpo))) 
            response.delete_cookie('encabezado')
            response.delete_cookie('cuerpo')
            
        return response
        '''return render_template("resistencias.html",form = resisForm, thead = mark_safe(thead),
                               tbody = mark_safe(tbody))'''


if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug = True, port = 3000)