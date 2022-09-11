from trusthouse.models.address import Address
from ..extensions import db

'''
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


get_address_object = create_new_address(door,street,location,postcode)


def address_object():
    return create_new_address()
'''

class CreateNewAddress:

    def __init__(self, door, street, location, postcode, new_address):
        self.door = door
        self.street = street
        self.location = location
        self.postcode = postcode
        self.new_address = new_address

        
    
    new_address = Address(
        door_num=door.lower(),
        street=self.street.lower(),
        location=location.lower(),
        postcode=postcode.lower(),
    )
    db.session.add(new_address)
    db.session.commit()

    get_address = 
    
