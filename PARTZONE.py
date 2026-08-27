from flask import flask 
PARTZONE =flask(__name__)
@PARTZONE.route('/')
def home();
        return '<h1>hello wordl</h1>'
        if __name__=='_main_':
            PARTZONE.run(port=1408,debug=True)
            