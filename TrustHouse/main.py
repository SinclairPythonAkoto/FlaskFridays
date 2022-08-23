from flask import Flask, render_template, url_for, request, redirect
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from cities import city
from towns import town

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
app.config["TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

'''
db queries

- Display all ratings 
get_ratings = [data.ratings for ratings in all_buildings]

- Display all reviews
get_reviews = Review.query.all()
for revs in all_reviews:
    revs.reviews, revs.reviewed_by
    revs.building.door_num etc

- Display all buildings
get_buidings = Building.query.all()
for buildings in all_buildings:
    building.door_num, building.street, etc

- Display all towns
get_towns = [data.town for data in all_buildings]
for town in get_towns:
    town

- display all cities
get_cities = [data.city for data in all_buildings]
for city in get_cities:
    city

- Display all postcodes
get_postcodes = [data.postcode for postcode in all_buildings]
for postcode in get_postcode:
    postcode

- Search via door numbers 
filter_door = Building.query.filter_by(door=filter_door).all()
filter_door[0].door_num / filter_door[0].street / etc (for a for loop, follow steps above)

- Search via street name
filter_street = Building.query.filter_by(street=filter_street).all()

- Search via town
filter_town = Building.query.filter_by(town=filter_town).all()

- Search via city
filter_city = Building.query.filter_by(city=filter_city).all()

- Search via postcode
filter_postcode = Builiding.query.filter_by(postcode=filter_postcode).all()
'''

# proprty table
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    town = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(10), nullable=False)
    reviews = db.relationship('Review', backref='building')

    def __init__(self, door_num, street, town, city, postcode):
        self.door_num = door_num
        self.street = street
        self.town = town
        self.city = city
        self.postcode = postcode

# review table
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    reviewed_by = db.Column(db.String(20), nullable=False)
    picture_data = db.Column(db.LargeBinary)
    rendered_pic = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

    def __init__(self, rating, review, reviewed_by, picture_data, rendered_pic, date):
        self.rating = rating
        self.review = review
        self.reviewed_by = reviewed_by
        self.picture_data = picture_data
        self.rendered_pic = rendered_pic
        self.date = date

# homepage to write a new review
class Home(MethodView):
    def get(self):
        # show page to write a review, href to send people to view reviews on page
        return render_template('writeReview.html')
    
    def post(self):
        # collect all the data from the form to add & query db
        review_content = request.form['reviewContent']
        review_rating = request.form['reviewRating']
        reviewed_by = request.form['reviewer']
        date = datetime.now()
        door = request.form['doorNumber']
        street_name = request.form['streetName']
        town_name = request.form['townName']
        city_name = request.form['cityName']
        review_postcode = request.form['reviewPostcode']

        return render_template('writeReview.html')

class DisplayReviews(MethodView):
    def get(self):
        # return all reviews as default
        return 'Display all reviews from Trust House'

    def post(self):
        return 'filter & search for review via user entries'

# define web route from class routes 
app.add_url_rule('/', view_func=Home.as_view(name='homepage'))
app.add_url_rule('/reviews', view_func=DisplayReviews.as_view(name='all_reviews'))

if '__main__' == __name__:
    db.create_all()
    app.run(debug=True)