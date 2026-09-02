from flask import Flask, render_template 
from flask_mysqldb import MySQL
from config import config

PARTZONE =Flask(__name__)
PARTZONE.config.from_object(config['development'])
db = MySQL(PARTZONE)

@PARTZONE.route('/')
def home():
    return render_template('home.html')

if __name__== '__main__':
    PARTZONE.run(port=1408,debug=True)

            