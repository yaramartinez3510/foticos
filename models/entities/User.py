from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, id, nombre, correo, clave, perfil, telefono=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.perfil = perfil
        self.telefono = telefono

    @staticmethod
    def validarClave(claveCifrada, clave):
        return bool(claveCifrada) and check_password_hash(claveCifrada, clave)
