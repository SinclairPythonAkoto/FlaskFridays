from flask import Flask  
from flaskwebgui import FlaskUI
from views.hello import hello
from views.homepage import homepage


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sportsPY.sqlite3"
app.config["TRACK_MODIFICATIONS"] = False


app.register_blueprint(hello, prefix="/")
app.register_blueprint(homepage, prefix="/home")


if __name__ == "__main__":

    debug = False

    if debug:
        app.run(debug=True)
    else:
        FlaskUI(app, width=500, height=500, start_server="flask").run() 
    
   