from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
db = dbase.dbConnection()
app = Flask(__name__)

#Datos para hoja NOSOTROS
from data.data_general import personal_data

@app.route("/")
def home():
    return render_template('/index.html')

#COMO LLEGAR
@app.route('/como_llegar')
def como_llegar():
    return render_template('como_llegar.html')

@app.route('/reservas')
def reservar():
    return render_template('reservas.html')

@app.route('/reservas/agregar', methods=["POST"])
def agregar_reserva():
    reservaciones = db["reservas"]
    nombre = request.form["nombre"]
    fecha_ingreso = request.form["fecha_ingreso"]
    fecha_salida = request.form["fecha_salida"]
    habitaciones = request.form["habitaciones"]

    if nombre and fecha_ingreso and fecha_salida and habitaciones:
        reserva = Reserva(nombre, fecha_ingreso, fecha_salida, habitaciones)
        reservaciones. insert_one(reserva.toDBCollecton())
        response= jsonify({
            "nombre": nombre,
            "fecha_ingreso": fecha_ingreso,
            "fecha_salida": fecha_salida,
            "habitaciones":habitaciones
        })
        return redirect(url_for("home"))
    else:
        return notFound()


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'mesage': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code=404
    return response
#lanzar la app
if __name__ == '__main__':
    app.run(debug=True, port=4000)