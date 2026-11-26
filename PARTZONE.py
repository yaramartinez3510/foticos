from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from werkzeug.security import generate_password_hash
from models.ModelUser import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.ModelUser import ModelUser
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
        # perfil = 'U'  # 'U' = usuario normal (ajústalo a la convención que uses, p. ej. 'A' = admin)

        #regUser = db.connection.cursor()
        #try:
            #regUser.execute(
             #   "INSERT INTO usuario (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)",
             #   (nombre, correo, claveCifrada, perfil)
           # )
           # db.connection.commit()
            #flash('¡Cuenta creada correctamente!', 'success')
        #except Exception as e:
          #  db.connection.rollback()
           # flash('Ese correo ya está registrado.', 'danger')
        #finally:
           # regUser.close()

        # Patrón POST-Redirect-GET: evita que al recargar se reenvíe el formulario
        return redirect(url_for('home'))

@PARTZONEApp.route('/sigin', methods=['GET', 'POST'])
def sigin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None)
        usuarioAutenticado = ModelUser.sigin(db, usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
            login_user(usuarioAutenticado)
            if usuarioAutenticado.perfil == 'A':
                return redirect(url_for('home_admin'))
            else:
                flash('Contraseña incorrecta')
                redirect(url_for('home'))
        else:
            flash('Usuario no encontrado')
            redirect(url_for('home'))

    return redirect(url_for('home'))
@PARTZONEApp.route('/iUsuario', methods=['GET', 'POST'])
@login_required 
def iUsuario():
    if request.method == 'POST' and current_user.perfil== 'A':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        perfil = request.form['perfil']
        regUsuario =db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario(nombre, correo, clave, perfil) VALUES ( %s, $s, $s, $s)", (nombre, correo, claveCifrada))
        db.connection.comit()
        regUsuario.close()
        flash('Usuario Registrado Correctamente')
        return redirect(url_for('sUsuario')) 
    else:
        return redirect (url_for('home'))
@PARTZONEApp.route('/iUsuario/<int:id>', methods=['GET', 'POST'])
@login_required 
def uUsuario(id):
    if request.method == 'POST' and current_user.perfil== 'A':
        nombre = request.form['nombre']
        correo = request.form['correo']
        perfil = request.form['perfil']
        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET nombre=%s, correo=%s, perfil=%s WHERE id=%s")
        db.connection.commit()
        actUsuario.close()
        flash("usuario actualizado correctamente")
        return redirect(url_for('sUsuario'))
    else:
        return redirect(url_for('home'))
@PARTZONEApp.route('/dUsuario', methods=['GET', 'POST'])
@login_required 
def dUsuario():
    if request.method == 'POST' and current_user.perfil== 'A':
        delUsuario = db.connection.cursor()
        delUsuario.execute("DELETE FROM usuario WHERE id=%s", (id))
        db.connection.commit()
        delUsuario.close()
        flash("Usuario eliminado correctamente")
        return redirect(url_for('sUsuario'))
    else:
        return redirect(url_for('home'))   
if __name__ == '__main__':
    PARTZONEApp.run(port=1408, debug=True)
