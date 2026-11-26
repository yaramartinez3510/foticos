from models.entities.User import User


class ModelUser:
    @classmethod
    def signin(cls, db, usuario):
        cursor = db.connection.cursor()
        try:
            cursor.execute(
                'SELECT id, nombre, correo, clave, perfil, telefono '
                'FROM usuario WHERE correo = %s',
                (usuario.correo,),
            )
            fila = cursor.fetchone()
            if fila is None or not User.validarClave(fila[3], usuario.clave):
                return None
            return User(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
        finally:
            cursor.close()

    @classmethod
    def get_by_id(cls, db, id):
        cursor = db.connection.cursor()
        try:
            cursor.execute(
                'SELECT id, nombre, correo, clave, perfil, telefono '
                'FROM usuario WHERE id = %s',
                (id,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return User(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
        finally:
            cursor.close()

    @classmethod
    def get_all(cls, db):
        cursor = db.connection.cursor()
        try:
            cursor.execute(
                'SELECT id, nombre, correo, perfil, telefono '
                'FROM usuario ORDER BY id'
            )
            return [
                User(fila[0], fila[1], fila[2], None, fila[3], fila[4])
                for fila in cursor.fetchall()
            ]
        finally:
            cursor.close()


