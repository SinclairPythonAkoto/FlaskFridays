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
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    reviews = db.relationship('Review', backref='address')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False, unique=True)
    reviewed_by = db.Column(db.String(20), nullable=False)
    picture_data = db.Column(db.LargeBinary)
    rendered_pic = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

@app.route("/")
def landingpage():
    return render_template("landingPage.html")

class Home(MethodView):
    def get(self):
        return render_template('homePage.html')
    
class WriteReview(MethodView):
    def get(self):
        return render_template('writeReviewPage.html')
    
    def post(self):
        # address data
        door = request.form['propertyNumber']
        street_name = request.form['streetName']
        town_city = request.form['town_city']
        postcode = request.form['postcode']
        # review data
        review_rating = request.form['rating']
        review_text = request.form['reviewText']
        review_type = request.form['selection']
        review_pic = request.form['imgUpload']

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()
        get_review_content = Review.query.filter_by(review=review_text).all()

        if len(get_postcode) == 0:
            new_address = Address(
                door_num=door,
                street=street_name,
                location=town_city,
                postcode=postcode,
            )
            db.session.add(new_address)
            db.session.commit()
            new_review = Review(
                rating=review_rating,
                review=review_text,
                reviewed_by=review_type,
                date=datetime.now()
            )
            db.session.add(new_review)
            db.session.commit()
            message = 'Your review has been uploaded!'
            return message
        else:
            if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                if len(get_review_content) != 0:
                    void = 'Dupliacte Review: please check and change the content within your review.'
                    return void
            new_review = Review(
                rating=review_rating,
                review=review_text,
                reviewed_by=review_type,
                date=datetime.now()
            )
            db.session.add(new_review)
            db.session.commit()
            message = f'A new review has been added to: {get_door_num[0].door_num}, {get_postcode[0].postcode}'
            return message
                

@app.route('/viewReviews')
def view_reviews():
    return render_template('searchReviewPage.html')

class DisplayAllReviews(MethodView):
    def post(self):
        get_reviews = Review.query.all()
        return render_template('searchReviewPage.html', get_reviews=get_reviews)


app.add_url_rule('/home', view_func=Home.as_view(name='homepage'))
app.add_url_rule('/writeReview', view_func=WriteReview.as_view(name='write_review'))
app.add_url_rule('/reviews/all', view_func=DisplayAllReviews.as_view(name='all_reviews'))


if __name__ == "__main__":
    app.run(debug=True)