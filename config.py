import os


class Config:
    SECRET_KEY = os.environ.get(
        'PARTZONE_SECRET_KEY', 'clave-local-partzone-cambiar-para-publicacion'
    )
    DEBUG = True

class DevelopmentConfig(Config):
    MYSQL_HOST = os.environ.get('PARTZONE_DB_HOST', '127.0.0.1')
    MYSQL_USER = os.environ.get('PARTZONE_DB_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('PARTZONE_DB_PASSWORD', '')
    MYSQL_DB = os.environ.get('PARTZONE_DB_NAME', 'partzone')
    MYSQL_PORT = int(os.environ.get('PARTZONE_DB_PORT', '3306'))
    MYSQL_CHARSET = 'utf8mb4'

config ={
    'development': DevelopmentConfig
}
