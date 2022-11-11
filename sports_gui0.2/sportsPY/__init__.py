from flask import Flask


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sportsPY.sqlite3"
app.config["TRACK_MODIFICATIONS"] = False


# user interface
import sportsPY.views.hello