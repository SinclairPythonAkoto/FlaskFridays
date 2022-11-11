from flask_sqlalchemy import SQLAlchemy
from sportsPY import app

db = SQLAlchemy()

db.init_app(app)