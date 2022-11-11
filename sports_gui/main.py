from flask import Flask  
from flask import render_template, request, url_for
from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# initialise the database
app.config['SECRET_KEY'] = 'somepassword'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportsgui.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = True
# creating database intsance
db = SQLAlchemy(app)

# create the db tables
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    student = db.relationship('Student', backref='students')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    result = db.relationship('Score', backref='results')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))


@app.route("/")
def hello():  
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def home(): 
    return render_template('some_page.html')

@app.route("/new_session", methods=['GET', 'POST'])
def new_session():
    if request.method == 'GET':
        return render_template('new_session.html')
    else:
        return "Your data has been sent"

@app.route("/view_table")
def view_table():
    return "View data table"

@app.route("/view_stats")
def view_stats():
    return "View stats & graphs from data tables"


if __name__ == "__main__":

    debug = False

    if debug:
        app.run(debug=True)
    else:
        FlaskUI(app, width=500, height=500, start_server="flask").run() 
    
   