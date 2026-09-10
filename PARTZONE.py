from flask import Flask, render_template, request, redirect 
from flask_mysqldb import MySQL
from config import config
from werkzeug.security import generate_password_hash

PARTZONEApp =Flask(__name__)
PARTZONEApp.config.from_object(config['development'])
db = MySQL(PARTZONEApp)

@PARTZONEApp.route('/')
def home():
    return render_template('home.html')

@PARTZONEApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave'] 
        claveCifrada = generate_password_hash(clave)
        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO usuario (nombre, correo, clave) VALUES (%s, %s, $s)", (nombre, correo, claveCifrada))
        db.connection.commit()
        return render_template('home.html')
    else:
        return render_template('home.html')

if __name__== '__main__':
    PARTZONEApp.run(port=1408,debug=True)

            