class Config:
    SECRET_KEY = 'contrasenasegura'
    DEBUG      = True

class DevelopmetConfig(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DATABASE = 'partzone'

config ={
    'development': DevelopmetConfig
}
