from trusthouse.models.address import Address
from ..extensions import db


def create_new_address(door, street, location, postcode):
    """
    Creates a new address, storing it in the Address table
    """
    new_address = Address(
                door_num=door.lower(),
                street=street.lower(),
                location=location.lower(),
                postcode=postcode.lower(),
            )
    db.session.add(new_address)
    db.session.commit()
    return new_address