from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
from models.mensaje import Mensaje
db = dbase.dbConnection()
app = Flask(__name__)
from bson import ObjectId
#Datos para hoja NOSOTROS
from data.data_general import personal_data

@app.route("/")
def home():
    return render_template("index.html")

#HABITACIONES
@app.route('/habitaciones')
def ver_habitaciones():
    habitaciones_db = list(db.habitacion.find())
    return render_template('habitaciones.html', habitaciones=habitaciones_db)

#COMO LLEGAR
@app.route('/comollegar')
def como_llegar():
    return render_template('como_llegar.html')

@app.route('/gestion_reservas')
def gestion_reservas():
    reservas_db=list (db.reservas.find())
    return render_template('/admin/gestion_reservas.html', reservas =reservas_db)

#CONTACTO
@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

#GESTION CONTACTO
@app.route('/gestion_contacto')
def gestion_contacto():
    mensajes_db = list(db.mensajes.find())
    return render_template('admin/gestion_contacto.html', mensajes=mensajes_db)

#CONTACTO: POST
@app.route('/mensaje/agregar', methods=['POST'])
def agregar_mensaje():
    mensajes = db.mensajes
    asunto = request.form['asunto']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    mensaje = request.form['mensaje']
    estado = "Mensaje recibido"

    mensaje = Mensaje(asunto, nombre, apellido, correo, mensaje, estado)
    mensajes.insert_one(mensaje.to_db_collection())
    return redirect(url_for('home'))

@app.route('/estado_reserva', methods=['POST'])
def cambiar_estado():
    reserva_id=request.form.get['reserva_id']
    #db = dbase.dbConnection()
    collection = db['reservas']
    reserva = collection.find_one({"_id":ObjectId(reserva_id)})
    if reserva:
        collection.update_one({"_id": ObjectId(reserva_id)},{"$set":{"estado":"Aceptada"}})
        return "cambiado"
    else:
        return "error"
@app.route('/habitacion/<habitacion_id>', methods=['GET'])
def mostrar_detalle_habitacion(habitacion_id):
    habitacion_db= db.habitacion.find_one({'_id:objectId(habitacion_id)'})
    return render_template('detalle_habitacion.html', habitacion=habitacion_db)
@app.route('/gestion_reservas')
def gestion_reservas():
    reservas_db=list (db.reservas.find())
    return render_template('/admin/gestion_reservas.html', reservas =reservas_db)

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