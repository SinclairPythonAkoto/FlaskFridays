from flask import Flask 
from flask import render_template, url_for, request, jsonify
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
app.config["TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)


# db models
# residence --> town / postcode
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    residence = db.Column(db.String(50))
    postcode = db.Column(db.String(10), nullable=False)
    reviews = db.relationship('Review', backref='building')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False, unique=True)
    reviewed_by = db.Column(db.String(20), nullable=False)
    picture_data = db.Column(db.LargeBinary)
    rendered_pic = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

@app.route("/")
def landingpage():
    return render_template("landingPage.html")



@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/writeReview")
def writeReview():
    return render_template('writeReviewPage.html')

@app.route('/viewReviews')
def view_reviews():
    return render_template('searchReviewPage.html')

if __name__ == "__main__":
    app.run(debug=True)