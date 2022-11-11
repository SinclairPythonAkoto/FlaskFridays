from flask import Flask  
from flaskwebgui import FlaskUI
from views.hello import hello


app = Flask(__name__)

app.register_blueprint(hello, prefix="/")


if __name__ == "__main__":

    debug = False

    if debug:
        app.run(debug=True)
    else:
        FlaskUI(app, width=500, height=500, start_server="flask").run() 
    
   