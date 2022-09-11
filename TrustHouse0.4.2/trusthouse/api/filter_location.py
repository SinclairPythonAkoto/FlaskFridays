from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_location import validate_location_request
from flask import jsonify
from ..extensions import app


class FilterByLocationAPI(MethodView):
    def get(self, location):
        user_location_request = location
        response = validate_location_request(user_location_request)
        if response == False:
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
                    'Type': review.type,
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
        data = {'Reviews by location': res}
        return jsonify(data)

app.add_url_rule(
    '/api/location/<location>',
    view_func=FilterByLocationAPI.as_view(
        name='filter_location_API'
    ),
)