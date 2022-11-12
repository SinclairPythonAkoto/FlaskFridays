from flask_sqlalchemy import SQLAlchemy
from main import app


db = SQLAlchemy()

db.init_app(app)

with app.app_context():
    db.create_all()