import re

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from werkzeug.security import generate_password_hash

from config import config
from models.ModelUser import ModelUser
from models.entities.User import User


PARTZONEApp = Flask(__name__)
PARTZONEApp.config.from_object(config['development'])
db = MySQL(PARTZONEApp)

login_manager = LoginManager(PARTZONEApp)
login_manager.login_view = 'home'
login_manager.login_message = 'Inicia sesión para continuar.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def cargar_usuario(id_usuario):
    return ModelUser.get_by_id(db, id_usuario)


def es_administrador():
    return current_user.is_authenticated and current_user.perfil == 'A'


def correo_valido(correo):
    return (
        len(correo) <= 150
        and re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', correo) is not None
    )


@PARTZONEApp.route('/')
@PARTZONEApp.route('/home')
def home():
    return render_template('home.html')


@PARTZONEApp.route('/signup', methods=['POST'])
def signup():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip().lower()
    telefono = re.sub(r'\D', '', request.form.get('telefono', ''))
    clave = request.form.get('clave', '')
    terminos = request.form.get('terminos') == 'si'

    if (
        not nombre
        or len(nombre) > 150
        or not correo
        or not clave
        or len(telefono) != 10
        or not terminos
    ):
        flash('Completa todos los campos y escribe un teléfono de 10 dígitos.', 'danger')
        return redirect(url_for('home'))
    if not correo_valido(correo):
        flash('Escribe un correo electrónico válido.', 'danger')
        return redirect(url_for('home'))
    if len(clave) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
        return redirect(url_for('home'))

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            'INSERT INTO usuario (nombre, correo, telefono, clave, perfil) '
            'VALUES (%s, %s, %s, %s, %s)',
            (nombre, correo, telefono, generate_password_hash(clave), 'U'),
        )
        db.connection.commit()
        flash('¡Cuenta creada correctamente! Ya puedes iniciar sesión.', 'success')
    except IntegrityError:
        db.connection.rollback()
        flash('Ese correo ya está registrado.', 'danger')
    except Exception:
        db.connection.rollback()
        PARTZONEApp.logger.exception('No se pudo registrar el usuario.')
        flash('No se pudo completar el registro. Revisa que MySQL esté iniciado.', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('home'))


@PARTZONEApp.route('/login', methods=['POST'])
def login():
    correo = request.form.get('correo', '').strip().lower()
    clave = request.form.get('clave', '')

    if not correo or not clave:
        flash('Escribe tu correo y contraseña.', 'danger')
        return redirect(url_for('home'))

    usuario = User(None, '', correo, clave, '')
    usuario = ModelUser.signin(db, usuario)
    if usuario is None:
        flash('El correo o la contraseña son incorrectos.', 'danger')
        return redirect(url_for('home'))

    login_user(usuario, remember=request.form.get('recordarme') == 'on')
    flash('Sesión iniciada correctamente.', 'success')
    return redirect(url_for('home'))


@PARTZONEApp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('home'))


@PARTZONEApp.route('/sUsuario')
@login_required
def sUsuario():
    if not es_administrador():
        flash('Solo una cuenta administradora puede consultar usuarios.', 'danger')
        return redirect(url_for('home'))

    usuarios = ModelUser.get_all(db)
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            'SELECT id_aviso, correo, marca, modelo, fecha '
            'FROM aviso_disponibilidad ORDER BY fecha DESC'
        )
        avisos = cursor.fetchall()
    finally:
        cursor.close()
    return render_template('usuarios.html', usuarios=usuarios, avisos=avisos)


@PARTZONEApp.route('/aviso', methods=['POST'])
def solicitar_aviso():
    correo = request.form.get('correo', '').strip().lower()
    marca = request.form.get('marca', '').strip()
    modelo = request.form.get('modelo', '').strip()
    if (
        not correo_valido(correo)
        or not marca
        or not modelo
        or len(marca) > 100
        or len(modelo) > 100
    ):
        flash('Escribe un correo, la marca y el modelo de tu vehículo.', 'danger')
        return redirect(url_for('home'))

    id_usuario = current_user.id if current_user.is_authenticated else None
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            'INSERT INTO aviso_disponibilidad (correo, marca, modelo, id_usuario) '
            'VALUES (%s, %s, %s, %s)',
            (correo, marca, modelo, id_usuario),
        )
        db.connection.commit()
        flash('Solicitud guardada. La tienda podrá contactarte cuando localice la pieza.', 'success')
    except Exception:
        db.connection.rollback()
        PARTZONEApp.logger.exception('No se pudo guardar la solicitud de disponibilidad.')
        flash('No se pudo guardar la solicitud. Revisa que MySQL esté iniciado.', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('home'))


@PARTZONEApp.route('/iUsuario', methods=['GET', 'POST'])
@login_required
def iUsuario():
    if not es_administrador():
        flash('Solo una cuenta administradora puede registrar usuarios.', 'danger')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return redirect(url_for('sUsuario'))

    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip().lower()
    telefono = re.sub(r'\D', '', request.form.get('telefono', ''))
    clave = request.form.get('clave', '')
    perfil = request.form.get('perfil', 'U')
    if perfil not in ('A', 'U'):
        perfil = 'U'
    if (
        not nombre
        or len(nombre) > 150
        or not correo_valido(correo)
        or len(telefono) != 10
        or len(clave) < 6
    ):
        flash('Revisa el nombre, correo, teléfono y contraseña.', 'danger')
        return redirect(url_for('sUsuario'))

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            'INSERT INTO usuario (nombre, correo, telefono, clave, perfil) '
            'VALUES (%s, %s, %s, %s, %s)',
            (nombre, correo, telefono, generate_password_hash(clave), perfil),
        )
        db.connection.commit()
        flash('Usuario registrado correctamente.', 'success')
    except IntegrityError:
        db.connection.rollback()
        flash('Ese correo ya está registrado.', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('sUsuario'))


@PARTZONEApp.route('/iUsuario/<int:id>', methods=['POST'])
@login_required
def uUsuario(id):
    if not es_administrador():
        flash('Solo una cuenta administradora puede actualizar usuarios.', 'danger')
        return redirect(url_for('home'))

    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip().lower()
    perfil = request.form.get('perfil', 'U')
    telefono = re.sub(r'\D', '', request.form.get('telefono', ''))
    if perfil not in ('A', 'U'):
        perfil = 'U'
    if not nombre or len(nombre) > 150 or not correo_valido(correo) or len(telefono) != 10:
        flash('Revisa el nombre, correo y teléfono.', 'danger')
        return redirect(url_for('sUsuario'))

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            'UPDATE usuario SET nombre=%s, correo=%s, telefono=%s, perfil=%s WHERE id=%s',
            (nombre, correo, telefono, perfil, id),
        )
        db.connection.commit()
        flash('Usuario actualizado correctamente.', 'success')
    except IntegrityError:
        db.connection.rollback()
        flash('Ese correo ya pertenece a otra cuenta.', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('sUsuario'))


@PARTZONEApp.route('/dUsuario/<int:id>', methods=['POST'])
@login_required
def dUsuario(id):
    if not es_administrador():
        flash('Solo una cuenta administradora puede eliminar usuarios.', 'danger')
        return redirect(url_for('home'))
    if str(current_user.get_id()) == str(id):
        flash('No puedes eliminar la cuenta con la que tienes la sesión abierta.', 'danger')
        return redirect(url_for('sUsuario'))

    cursor = db.connection.cursor()
    try:
        cursor.execute('DELETE FROM usuario WHERE id=%s', (id,))
        db.connection.commit()
        flash('Usuario eliminado correctamente.', 'success')
    except IntegrityError:
        db.connection.rollback()
        flash('No se puede eliminar este usuario porque tiene pedidos relacionados.', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('sUsuario'))


if __name__ == '__main__':
    PARTZONEApp.run(host='127.0.0.1', port=1408, debug=True)
