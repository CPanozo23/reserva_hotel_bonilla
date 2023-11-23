from bson import ObjectId
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
db = dbase.dbConnection()
app = Flask(__name__)

#Datos para hoja NOSOTROS
from data.data_general import personal_data

#COMO LLEGAR
@app.route('/como_llegar')
def como_llegar():
    return render_template('como_llegar.html')

@app.route('/gestion_reservas')
def gestion_reservas():
    reservas_db=list (db.reservas.find())
    return render_template('/admin/gestion_reservas.html', reservas =reservas_db)

@app.route('/estado_reserva/<reserva_id>', methods=['POST'])
def cambiar_estado_reserva(reserva_id):
    reservas = db.reservas
    id_obj = ObjectId(reserva_id)
    estado_actual = request.form ['estado']

    if estado_actual != "Anulado":
        if estado_actual == "Reservado":
            nuevo_estado = 'Confirmado'
        elif estado_actual == "Confirmado":
            nuevo_estado = 'Realizado'
        elif estado_actual == "Realizado":
            nuevo_estado = 'Anulado'

        reservas.update_one({'_id': id_obj}, {'$set': {'estado': nuevo_estado}})
    return redirect(url_for('gestion_reservas'))



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

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('user_info', None)
    return redirect(url_for('login'))