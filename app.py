from flask import Flask,render_template
from flask import request
from collections import Counter
import forms
import cajas

app = Flask(__name__)

@app.route("/formulario2",methods = ["GET"])
def formulario2():
    return render_template("formulario2.html")

@app.route("/Alumnos",methods = ["GET","POST"])
def alumno():
        alum_form = forms.UserForm(request.form)
        mat = ''
        nom = ''
        if request.method == 'POST':    
            print(alum_form.matricula.data)
            print(alum_form.nombre.data)
            #alum_form.form.apeP.data
            #alum_form.form.apeM.data
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
                    if (max_value is None or num > max_value):
                        print(num)
                        max_value = num

                min_value = None
                for num in numero:
                    if (min_value is None or num <= min_value):
                        print(num)
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

if __name__ == "__main__":
    app.run(debug = True, port = 3000)