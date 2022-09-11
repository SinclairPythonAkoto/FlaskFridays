from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_postcode import validate_postcode_request
from flask import jsonify
from ..extensions import app


class FilterByPostcodeAPI(MethodView):
    def get(self, postcode):
        user_postcode_request = postcode
        response = validate_postcode_request(user_postcode_request)
        if response == False:
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
        data = {'Reviews by postcode': res}
        return jsonify(data)

app.add_url_rule(
    '/api/postocde/<postcode>',
    view_func=FilterByPostcodeAPI.as_view(
        name='filter_postcode_API'
    )
)