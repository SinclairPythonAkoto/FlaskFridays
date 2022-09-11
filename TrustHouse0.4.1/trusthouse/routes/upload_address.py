from flask.views import MethodView
from trusthouse.models.address import Address
from flask import render_template, request
from ..extensions import app, db


class UploadAddress(MethodView):
    def get(self):
        return render_template('newAddress.html')
    
    def post(self):
        door = request.form['doorNum']
        street_name = request.form['streetName']
        location = request.form['addressLocation']
        postcode = request.form['addressPostcode']

        # get data to check if new review already exists
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


app.add_url_rule(
    '/createAddress',
    view_func=UploadAddress.as_view(
        'upload_address',
    ),
)