from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.review import Review
from trusthouse.utils.validate_door import validate_door_request
from flask import render_template, request
from ..extensions import app, db


class FilterByDoorNumber(MethodView):
    def post(self):
        user_door_request = request.form['searchDoorNum']
        response = validate_door_request(user_door_request)
        if response == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_door = Review.query.all() 
        return render_template(
            'searchReviewPage.html',
            user_door_request=user_door_request,
            filter_door=filter_door,
        )


app.add_url_rule(
    '/reviews/door_number',
    view_func=FilterByDoorNumber.as_view(
        name='filter_door'
    ),
)