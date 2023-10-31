from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from models.reserva import Reserva
db = dbase.dbConnection()
app = Flask(__name__)

#Datos para hoja NOSOTROS
from data.data_general import personal_data

@app.route('/')
def home():
    return render_template('index.html')
#COMO LLEGAR
@app.route('/como_llegar')
def como_llegar():
    return render_template('como_llegar.html')


@app.route('/nosotros')
def nosotros():
    data_array = personal_data
    def personal_data():
        return [
            {"nombre": "Marge Simpson", "cargo": "Gerente general"},
            {"nombre": "Homero J. Simpson", "cargo": "Recepcionista Senior"},
            {"nombre": "Bartolomeo Simpson", "cargo": "Chef"},
        ]
    return render_template('nosotros.html', objet_array=data_array)

@app.route('/login')
def contacto():
    return render_template('contacto.hlmn')
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