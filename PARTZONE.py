from flask import Flask, render_template 

PARTZONE =Flask(__name__)

@PARTZONE.route('/')
def home():
    return "hola mundo"

if __name__== '__main__':
    PARTZONE.run(port=1408,debug=True)
            