from functools import cached_property
from re import L
from flask import Flask, render_template, url_for, request, jsonify
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

# review table
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False, unique=True)
    reviewed_by = db.Column(db.String(20), nullable=False)
    picture_data = db.Column(db.LargeBinary)
    rendered_pic = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))

    # @cached_property
    # def get_town(self):
    #     return self.building.town
    

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
        door = request.form['doorNumber']
        street_name = request.form['streetName']
        town_name = request.form['townName']
        city_name = request.form['cityName']
        review_postcode = request.form['reviewPostcode']

        '''
        Before we add the information to the db, we need to check if there
        is an address already existing in the db.  If there is a matching 
        address then the review will be added to it's relationship.

        If matching door number & matching postcode, add review to matching address.
        If they do not match, create a new entry for the address & review
        '''

        # get data from the db to check if they already exist
        get_door_number = Building.query.filter_by(door_num=door).all()
        get_postcode = Building.query.filter_by(postcode=review_postcode).all()
        get_review_conent = Review.query.filter_by(review=review_content).all()
        print(len(get_postcode))
        # rearrange try block --> if statement, if len poscode is 0 then create a new entry
        # else, 
        # if door & poscode match, and there is a duplicate warn the user, else add new review to existing address
        if len(get_postcode) == 0:
            new_address = Building(
                door_num=door,
                street=street_name,
                town=town_name,
                city=city_name,
                postcode=review_postcode,
            )
            db.session.add(new_address)
            db.session.commit()
            new_review = Review(
                rating=review_rating,
                review=review_content,
                reviewed_by=reviewed_by,
                date=datetime.now(),
                building=new_address,
            )
            db.session.add(new_review)
            db.session.commit()
            message = 'Your review has been uploaded!'
            return message
        else:    
            if door == get_door_number[0].door_num and review_postcode == get_postcode[0].postcode:
                # need to use a try block to check if the review content is not a duplicate
                if len(get_review_conent) != 0:
                    message = 'DUPLICATE REVIEW: please check & change the content within your review'
                    return message
                new_review = Review(
                    rating=review_rating,
                    review=review_content,
                    reviewed_by=reviewed_by,
                    date=datetime.now(),
                    building=get_postcode[0],
                )
                db.session.add(new_review)
                db.session.commit()
                message = f'A new review has been added to: {get_postcode[0].door_num}, {get_postcode[0].street}'
                return message
            
            
class DisplayReviews(MethodView):
    def get(self):
        # return all reviews as default
        return render_template('viewReview.html')

# display all reviws
class DisplayAllReviews(MethodView):
    def post(self):
        get_reviews = Review.query.all()
        return render_template('viewReview.html', get_reviews=get_reviews)


# display all towns listed
class DisplayAllTowns(MethodView):
    def post(self):
        listed_towns = Building.query.all()
        return render_template('viewREview.html', listed_towns=listed_towns)


# display all cities listed
class DisplayAllCites(MethodView):
    def post(self):
        listed_cities = Building.query.all()
        return render_template('viewReview.html', listed_cities=listed_cities)


# filter by review rating
class FilterByRating(MethodView):
    def post(self):
        user_rating_rquest = request.form['searchRating']
        user_rating_rquest = int(user_rating_rquest)
        check_val = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_rquest).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        get_ratings = db.session.query(Review).filter_by(rating=user_rating_rquest).all()
        return render_template('viewReview.html', get_ratings=get_ratings)


# filter by door number
class FilterByDoorNumber(MethodView):
    def post(self):
        user_door_request = request.form['searchDoorNumber']
        check_val = db.session.query(
            db.session.query(Building).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        filter_door = Review.query.all()
        return render_template('viewReview.html', filter_door=filter_door, user_door_request=user_door_request)

# filter street name
class FilterByStreetName(MethodView):
    def post(self):
        user_street_request = request.form['searchStreetName']
        check_val = db.session.query(
            db.session.query(Building).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        filter_street = Review.query.all()
        return render_template('viewReview.html', user_street_request=user_street_request, filter_street=filter_street)
        

# filter town
class FilterByTown(MethodView):
    def post(self):
        user_town_request = request.form['searchTown']
        check_val = db.session.query(
            db.session.query(Building).filter_by(town=user_town_request).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        filter_town = Review.query.all()
        return render_template('viewReview.html', user_town_request=user_town_request, filter_town=filter_town)


# filter city
class FilterByCity(MethodView):
    def post(self):
        user_city_request = request.form['searchCity']
        check_val = db.session.query(
            db.session.query(Building).filter_by(city=user_city_request).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        filter_city = Review.query.all()
        return render_template('viewReview.html', user_city_request=user_city_request, filter_city=filter_city)

# filter postcode
class FilterByPostcode(MethodView):
    def post(self):
        user_postcode_request = request.form['searchPostcode']
        check_val = db.session.query(
            db.session.query(Building).filter_by(postcode=user_postcode_request).exists()
        ).scalar()
        if check_val == False:
            void = 'no match found'
            return render_template('viewReview.html', void=void)
        filter_postcode = Review.query.all()
        return render_template('viewReview.html', user_postcode_request=user_postcode_request, filter_postcode=filter_postcode)


'''
Create the API calls for the user, to enable them to query reviews and get results from the browser.

- get all address
- get all reviews

- filter by specfic rating -> API/rating/<...>
- filter by door number --> API/door/<...>
- filter by street name --> API/street/<...>
- filter by town name --> API/town/<...>
- filter by city name --> API/city/<...>
- filter by postcode name --> API/postcode/<...>
'''

# @app.route('/API/address')
# def address_API():
#     return 'hello world'

class AllAddressesAPI(MethodView):
    def get(self):
        all_addresses = Building.query.all()
        res = []
        for address in all_addresses:
            result = {
                'id': address.id,
                'Door Number': address.door_num,
                'Street': address.street,
                'Town': address.town,
                'City': address.city,
                'Postcode': address.postcode
            }
            res.append(result)
        data = {'all addresses': res}
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
                'Building ID': review.building_id,
                'Address': {
                    'id': review.building.id,
                    'Door Number': review.building.door_num,
                    'Street': review.building.street,
                    'Postode': review.building.postcode,
                },
            }
            res.append(result)
        data = {'all reviews': res}
        return jsonify(data)


class FilterByRatingAPI(MethodView):
    def get(self, rating):
        user_rating_rquest = int(rating)
        check_val = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_rquest).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_ratings = db.session.query(Review).filter_by(rating=user_rating_rquest).all()
        for review in get_ratings:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Reviewed By': review.reviewed_by,
                'Date': review.date,
                'Building ID': review.building_id,
                'Address': {
                    'id': review.building.id,
                    'Door Number': review.building.door_num,
                    'Street': review.building.street,
                    'Postode': review.building.postcode,
                },
            }
            res.append(result)
        data = {'reviews by rating': res}
        return jsonify(data)


class FilterByDoorAPI(MethodView):
    def get(self, door_num):
        user_door_request = door_num
        check_val = db.session.query(
            db.session.query(Building).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_door_request == review.building.door_num:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Building ID': review.building_id,
                    'Address': {
                        'id': review.building.id,
                        'Door Number': review.building.door_num,
                        'Street': review.building.street,
                        'Postode': review.building.postcode,
                    },
                }
                res.append(result)
        data = {'search by door number': res}
        return jsonify(data)


class FilterByStreetAPI(MethodView):
    def get(self, street):
        user_street_request = street
        check_val = db.session.query(
            db.session.query(Building).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_street_request == review.building.street:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Building ID': review.building_id,
                    'Address': {
                        'id': review.building.id,
                        'Door Number': review.building.street,
                        'Street': review.building.street,
                        'Postode': review.building.postcode,
                    },
                }
                res.append(result)
        data = {'search by street': res}
        return jsonify(data)


class FilterByTownAPI(MethodView):
    def get(self, town):
        user_town_request = town
        check_val = db.session.query(
            db.session.query(Building).filter_by(town=user_town_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_town_request == review.building.town:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Building ID': review.building_id,
                    'Address': {
                        'id': review.building.id,
                        'Door Number': review.building.street,
                        'Street': review.building.street,
                        'Postode': review.building.postcode,
                    },
                }
                res.append(result)
        data = {'search by town': res}
        return jsonify(data)


class FilterByCityAPI(MethodView):
    def get(self, city):
        user_city_request = city
        check_val = db.session.query(
            db.session.query(Building).filter_by(city=user_city_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_city_request == review.building.city:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Building ID': review.building_id,
                    'Address': {
                        'id': review.building.id,
                        'Door Number': review.building.street,
                        'Street': review.building.street,
                        'Postode': review.building.postcode,
                    },
                }
                res.append(result)
        data = {'search by city': res}
        return jsonify(data)


class FilterByPostcodeAPI(MethodView):
    def get(self, postcode):
        user_postcode_request = postcode
        check_val = db.session.query(
            db.session.query(Building).filter_by(postcode=user_postcode_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_postcode_request == review.building.postcode:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Reviewed By': review.reviewed_by,
                    'Date': review.date,
                    'Building ID': review.building_id,
                    'Address': {
                        'id': review.building.id,
                        'Door Number': review.building.street,
                        'Street': review.building.street,
                        'Postode': review.building.postcode,
                    },
                }
                res.append(result)
        data = {'search by postcode': res}
        return jsonify(data)                


# define web route from class routes 
app.add_url_rule('/', view_func=Home.as_view(name='homepage'))
app.add_url_rule('/reviews', view_func=DisplayReviews.as_view(name='display_reviews'))
app.add_url_rule('/reviews/all', view_func=DisplayAllReviews.as_view(name='all_reviews'))
app.add_url_rule('/reviews/listed-towns', view_func=DisplayAllTowns.as_view(name='listed_towns'))
app.add_url_rule('/reviews/listed-cities', view_func=DisplayAllCites.as_view(name='listed_cities'))
app.add_url_rule('/reviews/rating', view_func=FilterByRating.as_view(name='filter_rating'))
app.add_url_rule('/reviews/door_number', view_func=FilterByDoorNumber.as_view(name='filter_door_num'))
app.add_url_rule('/reviews/street', view_func=FilterByStreetName.as_view(name='filter_street'))
app.add_url_rule('/reviews/town', view_func=FilterByTown.as_view(name='filter_town'))
app.add_url_rule('/reviews/city', view_func=FilterByCity.as_view(name='filter_city'))
app.add_url_rule('/reviews/postcode', view_func=FilterByPostcode.as_view(name='filter_postcode'))
# API routes:
app.add_url_rule('/API/address', view_func=AllAddressesAPI.as_view(name='address_API'))
app.add_url_rule('/API/reviews', view_func=AllReviewsAPI.as_view(name='review_API'))
app.add_url_rule('/API/rating/<rating>', view_func=FilterByRatingAPI.as_view(name='filter_by_rating_API'))
app.add_url_rule('/API/door/<door_num>', view_func=FilterByDoorAPI.as_view(name='filter_by_door_API'))
app.add_url_rule('/API/street/<street>', view_func=FilterByStreetAPI.as_view(name='filtesr_by_street_API'))
app.add_url_rule('/API/town/<town>', view_func=FilterByTownAPI.as_view(name='filter_by_town_API'))
app.add_url_rule('/API/city/<city>', view_func=FilterByCityAPI.as_view(name='filter_by_city_API'))
app.add_url_rule('/API/postcode/<postcode>', view_func=FilterByPostcodeAPI.as_view(name='filter_by_postcode_API'))


if '__main__' == __name__:
    db.create_all()
    # first_address = Building(
    #     door_num='18',
    #     street='Kingly Street',
    #     town='Soho',
    #     city='London',
    #     postcode='W18 5PX',
    # )
    # first_review = Review(
    #     rating=3,
    #     review='Your review goes here...',
    #     reviewed_by='tenant',
    #     date=datetime.now(),
    #     building=first_address,
    # )
    # default_data = [first_address, first_review]
    # db.session.add_all(default_data)
    # db.session.commit()
    app.run(debug=True)