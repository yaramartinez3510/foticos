from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from config import config
from werkzeug.security import generate_password_hash

PARTZONEApp = Flask(__name__)
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
        perfil = 'U'  # 'U' = usuario normal (ajústalo a la convención que uses, p. ej. 'A' = admin)

        regUser = db.connection.cursor()
        try:
            regUser.execute(
                "INSERT INTO usuario (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)",
                (nombre, correo, claveCifrada, perfil)
            )
            db.connection.commit()
            flash('¡Cuenta creada correctamente!', 'success')
        except IntegrityError:
            db.connection.rollback()
            flash('Ese correo ya está registrado.', 'danger')
        finally:
            regUser.close()

        # Patrón POST-Redirect-GET: evita que al recargar se reenvíe el formulario
        return redirect(url_for('home'))

    return redirect(url_for('home'))

if __name__ == '__main__':
    PARTZONEApp.run(port=1408, debug=True)
