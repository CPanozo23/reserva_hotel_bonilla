from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
db = dbase.dbConnection()
app = Flask(__name__)
from bson import ObjectId
#Datos para hoja NOSOTROS
from data.data_general import personal_data

@app.route('/')
def home ():
    return render_template('index.html')
#sdfsf
#HABITACIONES
@app.route('/habitaciones')
def ver_habitaciones():
    habitaciones_db = list(db.habitacion.find())
    return render_template('habitaciones.html', habitaciones=habitaciones_db)

#COMO LLEGAR
@app.route('/como_llegar')
def como_llegar():
    return render_template('como_llegar.html')

@app.route('/habitacion/<habitacion_id>', methods=['GET'])
def mostrar_detalle_habitacion(habitacion_id):
    habitacion_db= db.habitacion.find_one({'_id:objectId(habitacion_id)'})
    return render_template('detalle_habitacion.html', habitacion=habitacion_db)

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