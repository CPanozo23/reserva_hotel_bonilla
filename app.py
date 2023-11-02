from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
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

@app.route('/gestion_reservas')
def gestion_reservas():
    reservas_db=list (db.reservas.find())
    return render_template('/admin/gestion_reservas.html', reservas =reservas_db)

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