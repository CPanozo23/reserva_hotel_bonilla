from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
from models.mensaje import Mensaje
db = dbase.dbConnection()
app = Flask(__name__)

#Datos para hoja NOSOTROS
from data.data_general import personal_data

@app.route("/")
def home():
    return render_template("index.html")

#COMO LLEGAR
@app.route('/comollegar')
def como_llegar():
    return render_template('como_llegar.html')

#CONTACTO
@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

#GESTION CONTACTO
@app.route('/gestion_contacto')
def gestion_contacto():
    mensajes_db = list(db.mensajes.find())
    return render_template('admin/gestion_contacto.html', mensajes=mensajes_db)

###############################################################################################################################################################################

#CONTACTO: POST
@app.route('/mensaje/agregar', methods=['POST'])
def agregar_mensaje():
    mensajes = db.mensaje
    asunto = request.form['asunto']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    mensaje = request.form['mensaje']
    estado = "Mensaje recibido"

    mensaje = Mensaje(asunto, nombre, apellido, correo, mensaje, estado)
    mensajes.insert_one(mensaje.to_db_collection())
    return redirect(url_for('home'))



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