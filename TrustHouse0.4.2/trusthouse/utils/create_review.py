'''
 new_review = Review(
    rating=review_rating,
    review=review_text,
    type=review_type,
    date=datetime.now(),
    address=new_address,
)
db.session.add(new_review)
db.session.commit()
'''
from datetime import datetime
from trusthouse.models.review import Review
from ..extensions import db


def create_new_review(rating, review, review_type, address):
    """
    Creates a new review entry, storing it in the Review table.
    Each review is linked to the Address id.

    Returns the Review object after saving it.
    """
    new_review_entry = Review(
        rating=rating,
        review=review,
        type=review_type,
        date=datetime.now(),
        address=address,
    )
    db.session.add(new_review_entry)
    db.session.commit()
    return new_review_entry