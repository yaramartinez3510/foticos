class Config:
    SECRET_KEY = 'contrasenasegura'
    DEBUG      = True

class DevelopmentConfig(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB = 'partzone'

config ={
    'development': DevelopmentConfig
}
