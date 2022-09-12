from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.maps import Maps
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.validate_door import validate_door_request
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.request_messages import warning_message, error_message, ok_message
from flask import render_template, request, jsonify
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
        # get_door_num = Address.query.filter_by(door_num=door).all()
        # get_postcode = Address.query.filter_by(postcode=postcode).all()

        # use the validation functions to check if door & postcode match or not 
        door_request = validate_door_request(door)
        postcode_request = validate_postcode_request(postcode)
        # if there is no preexisting postcode create new address.
        if postcode_request == False:
            # write fuction
            new_address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=location.lower(),
                postcode=postcode.lower(),
            )
            db.session.add(new_address)
            db.session.commit()
            # write fuction
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            # write fuction
            if user_postcode_coordinates == None:
                # write fuction
                data = {
                    'Incomplete upload': warning_message()[0], 
                    'Status':warning_message()[1]
                }
                return jsonify(data)
            elif user_postcode_coordinates != None:
                latitude = user_postcode_coordinates[0].get('lat')
                longitude = user_postcode_coordinates[0].get('lon')
                new_geo_map = Maps(
                    lon=longitude,
                    lat=latitude,
                    location=new_address,
                )
                db.session.add(new_geo_map)
                db.session.commit()
                message = ok_message()[0]['Success']
                return render_template('newAddress.html', message=message)
            else:
                data = {
                    'Unexpecte error': error_message()[0],
                    'status': error_message()[0], 
                }
                return jsonify(data)
        else:
            if door_request == False and postcode_request == True:
                new_address = Address(
                    door_num=door.lower(),
                    street=street_name.lower(),
                    location=location.lower(),
                    postcode=postcode.lower(),
                )
                db.session.add(new_address)
                db.session.commit()
                user_postcode_coordinates = get_postcode_coordinates(postcode)
                # if there is an existing latitude & longitude
                if user_postcode_coordinates:
                    latitude = user_postcode_coordinates[0].get('lat')
                    longitude = user_postcode_coordinates[0].get('lon')
                    new_geo_map = Maps(
                        lon=longitude,
                        lat=latitude,
                        location=new_address,
                    )
                    db.session.add(new_geo_map)
                    db.session.commit()
                    message = ok_message()[0]['Success']
                    return render_template('newAddress.html', message=message)


app.add_url_rule(
    '/createAddress',
    view_func=UploadAddress.as_view(
        'upload_address',
    ),
)