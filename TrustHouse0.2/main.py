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
    review = db.Column(db.Text, nullable=False)
    reviewed_by = db.Column(db.String(20), nullable=False)
    picture_data = db.Column(db.LargeBinary)
    rendered_pic = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))


class LandingPage(MethodView):
    def get(self):
        return render_template('landingPage.html')

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
        review_rating = int(review_rating)
        review_text = request.form['reviewText']
        review_type = request.form['selection']
        review_pic = request.form['imgUpload']

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()
        get_review_content = Review.query.filter_by(review=review_text).all()

        if len(get_postcode) == 0:
            new_address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=town_city.lower(),
                postcode=postcode.lower(),
            )
            db.session.add(new_address)
            db.session.commit()
            new_review = Review(
                rating=review_rating,
                review=review_text,
                reviewed_by=review_type,
                date=datetime.now(),
                address=new_address,
            )
            db.session.add(new_review)
            db.session.commit()
            message = 'Your review has been uploaded!'
            return render_template('writeReviewPage.html', message=message)
        else:
            if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                if len(get_review_content) != 0:
                    new_review = Review(
                        rating=review_rating,
                        review=review_text,
                        reviewed_by=review_type,
                        date=datetime.now(),
                        address=get_postcode[0],
                    )
                    db.session.add(new_review)
                    db.session.commit()
                    message = 'A new review has been added to an existing postcode.'
                    return render_template('writeReviewPage.html', message=message)
                new_review = Review(
                    rating=review_rating,
                    review=review_text,
                    reviewed_by=review_type,
                    date=datetime.now(),
                    address=get_postcode[0],
                )
                db.session.add(new_review)
                db.session.commit()
                message = 'A new review has been added'
                return render_template('writeReviewPage.html', message=message)
                

class DisplayAllReviews(MethodView):
    def get(self):
        return render_template('searchReviewPage.html')
    def post(self):
        get_reviews = Review.query.all()
        return render_template('searchReviewPage.html', get_reviews=get_reviews)

class DisplayListedLocations(MethodView):
    def post(self):
        listed_locations = Address.query.all()
        return render_template('searchReviewPage.html', listed_locations=listed_locations)

class FilterByRating(MethodView):
    def post(self):
        user_rating_request = request.form['searchRating']
        user_rating_request = int(user_rating_request)
        check_request = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        get_ratings = db.session.query(Review).filter_by(rating=user_rating_request).all()
        return render_template('searchReviewPage.html', get_ratings=get_ratings)

class FilterByDoorNumber(MethodView):
    def post(self):
        user_door_request = request.form['searchDoorNum']
        check_request = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_door = Review.query.all() 
        return render_template(
            'searchReviewPage.html',
            user_door_request=user_door_request,
            filter_door=filter_door,
        )

class FilterByStreetName(MethodView):
    def post(self):
        user_street_request = request.form['searchStreetName']
        check_request = db.session.query(
            db.session.query(Address).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_street = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_street_request=user_street_request,
            filter_street=filter_street,
        )

class FilterByLocation(MethodView):
    def post(self):
        user_location_request = request.form['searchLocation']
        check_request = db.session.query(
            db.session.query(Address).filter_by(location=user_location_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_location = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_location_request=user_location_request,
            filter_location=filter_location,
        )

class FilterByPostcode(MethodView):
    def post(self):
        user_postcode_request = request.form['searchPostcode']
        check_request = db.session.query(
            db.session.query(Address).filter_by(postcode=user_postcode_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_postcode = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_postcode_request=user_postcode_request,
            filter_postcode=filter_postcode,
        )

class DisplayAllAddressesAPI(MethodView):
    def get(self):
        all_address = Address.query.all()
        db_query_result = []
        for address in all_address:
            result = {
                'id': address.id,
                'Door Number': address.door_num,
                'Street Name': address.street,
                'Location': address.location,
                'Postcode': address.postcode,
            }
            db_query_result.append(result)
        data = {'All Addresses': db_query_result}
        return jsonify(data)

class AllReviewsAPI(MethodView):
    def get(self):
        all_reviews = Review.query.all()
        res = []
        print(all_reviews)
        for review in all_reviews:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Reviewed By': review.reviewed_by,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.door_num,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            res.append(result)
        data = {'all reviews': res}
        return jsonify(data)

class FilterByRatingAPI(MethodView):
    def get(self, rating):
        user_rating_request = int(rating)
        check_request = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_request).exists()
        ).scalar()
        if check_request == False:
            void = {'Void': 'No match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Reviewed By': review.reviewed_by,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.door_num,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            res.append(result)
        data = {'Reviews by Door Number': res}
        return jsonify(data)

class FilterByDoorAPI(MethodView):
    def get(self, door):
        user_door_request = door
        check_val = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        print(get_reviews)
        for review in get_reviews:
            if user_door_request == review.address.door_num:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.door_num,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        data = {'search by door number': res}
        return jsonify(data)

class FilterByStreetAPI(MethodView):
    def get(self, street):
        user_street_request = street
        check_val = db.session.query(
            db.session.query(Address).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_street_request == review.address.street:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.street,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        data = {'search by street': res}
        return jsonify(data)

class FilterByLocationAPI(MethodView):
    def get(self, location):
        user_location_request = location
        check_val = db.session.query(
            db.session.query(Address).filter_by(location=user_location_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_location_request == review.address.location:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.street,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        data = {'search by location': res}
        return jsonify(data)    

class FilterByPostcodeAPI(MethodView):
    def get(self, postcode):
        user_postcode_request = postcode
        check_val = db.session.query(
            db.session.query(Address).filter_by(postcode=user_postcode_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_postcode_request == review.address.postcode:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.street,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        data = {'search by postcode': res}
        return jsonify(data)

class UploadAddressAPI(MethodView):
    def get(self):
        return render_template('newAddress.html')
    
    def post(self):
        door = request.form['doorNum']
        street_name = request.form['streetName']
        location = request.form['addressLocation']
        postcode = request.form['addressPostcode']

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()

        if len(get_postcode) == 0:
            new_address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=location.lower(),
                postcode=postcode.lower(),
            )
            db.session.add(new_address)
            db.session.commit()
            message = 'Your review has been uploaded!'
            return message
        else:
            if door == get_postcode[0].door_num and postcode == get_postcode[0].postcode:
                if len(get_postcode) != 0:
                    message = f'This address hass already been uploaded.'
                    return message
            elif door != get_postcode[0].door_num and postcode == get_postcode[0].postcode:
                new_address = Address(
                    door_num=door,
                    street=street_name,
                    location=location,
                    postcode=postcode,
                )
                db.session.add(new_address)
                db.session.commit()
                message = 'A new address has been uploaded to the postcode!'
                return message
            elif door == get_postcode[0].door_num and postcode != get_postcode[0].postcode:
                new_address = Address(
                    door_num=door,
                    street=street_name,
                    location=location,
                    postcode=postcode,
                )
                db.session.add(new_address)
                db.session.commit()
                message = 'A new address has been uploaded!'
                return message

app.add_url_rule('/', view_func=LandingPage.as_view(name='landingpage'))
app.add_url_rule('/home', view_func=Home.as_view(name='homepage'))
app.add_url_rule('/writeReview', view_func=WriteReview.as_view(name='write_review'))
app.add_url_rule('/viewReview', view_func=DisplayAllReviews.as_view(name='view_reviews'))
app.add_url_rule('/reviews/all', view_func=DisplayAllReviews.as_view(name='all_reviews'))
app.add_url_rule('/reviews/all/locations', view_func=DisplayListedLocations.as_view(name='listed_locations'))
app.add_url_rule('/reviews/rating', view_func=FilterByRating.as_view(name='filter_ratings'))
app.add_url_rule('/reviews/door_number', view_func=FilterByDoorNumber.as_view(name='filter_door'))
app.add_url_rule('/reviews/street', view_func=FilterByStreetName.as_view(name='filter_street'))
app.add_url_rule('/reviews/location', view_func=FilterByLocation.as_view(name='filter_location'))
app.add_url_rule('/reviews/postcode', view_func=FilterByPostcode.as_view(name='filter_postcode'))
# (get) API routes
app.add_url_rule('/API/address', view_func=DisplayAllAddressesAPI.as_view(name='display_address_API'))
app.add_url_rule('/API/reviews', view_func=AllReviewsAPI.as_view(name='review_API'))
app.add_url_rule('/API/rating/<rating>', view_func=FilterByRatingAPI.as_view(name='filter_rating_API'))
app.add_url_rule('/API/door/<door>', view_func=FilterByDoorAPI.as_view(name='filter_door_API'))
app.add_url_rule('/API/street/<street>', view_func=FilterByStreetAPI.as_view(name='filter_street_API'))
app.add_url_rule('/API/location/<location>', view_func=FilterByLocationAPI.as_view(name='filter_location_API'))
app.add_url_rule('/API/postcode/<postcode>', view_func=FilterByPostcodeAPI.as_view(name='filter_postcode_API'))
# (post) API route
app.add_url_rule('/createAddress', view_func=UploadAddressAPI.as_view(name='upload_address'))


if __name__ == "__main__":
    app.run(debug=True)