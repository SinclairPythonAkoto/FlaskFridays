from ..extensions import db

# one to one
class Maps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.String(15), nullable=False)
    lat = db.Column(db.String(15), nullable=False)
    addres_id = db.Column(db.Integer, db.ForeignKey('address.id'))