from flask import Flask, render_template, redirect, url_for, jsonify, session, request

app = Flask(__name__)

import database as dbase
from models.reserva import Reserva
from models.mensaje import Mensaje
db = dbase.dbConnection()
from bson import ObjectId
from datetime import datetime, timedelta 
#Datos para hoja NOSOTROS
from data.data_general import personal_data

#RUTAS USUARIOS NO REGISTRADOS
@app.route("/")
def home():
    return render_template("index.html")

#HABITACIONES
@app.route('/habitaciones')
def ver_habitaciones():
    habitaciones_db = list(db.habitacion.find())
    return render_template('habitaciones.html', habitaciones=habitaciones_db)
#RESERVAS
@app.route('/reservas')
def reservar():
    habitaciones_db = list(db.habitacion.find())
    return render_template('reservas.html', habitaciones=habitaciones_db, datetime=datetime, timedelta=timedelta) 

#COMO LLEGAR
@app.route('/como_llegar')
def como_llegar():
    return render_template('como_llegar.html')

#NOSOTROS
@app.route('/nosotros')
def nosotros():
    data_array = personal_data()
    return render_template('nosotros.html', data_array=data_array)

#CONTACTO
@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

#LOGIN
@app.route("/login")
def login():
    return render_template('login.html')

#HABITACIONES POR ID
@app.route('/habitacion/<habitacion_id>', methods=['GET'])
def mostrar_detalle_habitacion(habitacion_id):
    habitacion_db = db.habitacion.find_one({'_id': ObjectId(habitacion_id)})
    return render_template('detalle_habitaciones.html', habitacion=habitacion_db)

#RUTAS DE ADMINISTRADOR

#GESTION RESERVA
@app.route('/gestion_reservas')
def gestion_reservas():
    reservas_db=list (db.reservas.find())
    return render_template('/admin/gestion_reservas.html', reservas =reservas_db)

# GESTION CONTACTO
@app.route('/gestion_contacto')
def gestion_contacto():
    user_info = session.get('user_info')
    if user_info:
        mensajes_db = list(db.mensajes.find())
        return render_template('admin/gestion_contacto.html', mensajes=mensajes_db)
    else:
        return redirect(url_for('login'))
        redirect()

#INTERACCION CON BASE DE DATOS

#CONTACTO: POST
@app.route('/mensaje/agregar', methods=['POST'])
def agregar_mensaje():
    mensajes = db.mensaje
    asunto = request.form['asunto']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    mensaje = request.form['mensaje']
    estado = "Recibido"
    mensaje = Mensaje(asunto, nombre, apellido, correo, mensaje, estado)
    mensajes.insert_one(mensaje.to_db_collection())
    return redirect(url_for('home'))

#RESERVAS: post
@app.route('/reservas/agregar', methods={'POST'}) 
def agregar_reserva():
    reservaciones = db.reservas
    nombre = request.form['nombre']
    apellido = request.form['apellido'] 
    fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d')
    fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
    habitaciones_db = list(db.habitacion.find())
    habitaciones = [] 

    if fecha_salida <= fecha_ingreso: 
        error_message = 'error: la fecha de salida debe ser posterior a laq fecha de ingreso,'
        return render_template('reservas.html', error_message=error_message, habitaciones=habitaciones_db)
    
    if (fecha_salida - fecha_ingreso).days < 1:
        error_message = 'Error: la reserva debe ser de al menos un  dia.'
        return render_template('reservas.html', error_message=error_message, habitaciones=habitaciones_db)
    
    habitaciones_cantidad = False
    for habitacion in habitaciones_db:
        cantidad = request.form.get(f"cantidad_{habitacion['nombre']}")
        if cantidad and 1 <= int(cantidad) <= 10:
            habitacion_cantidad = True 
            habitaciones.append({
                "nombre": habitacion['nombre'],
                "valor": habitacion['precio'],
                "cantidad": int(cantidad)
            })

#RESERVAS: CAMBIAR ESTADO CON POST
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
    