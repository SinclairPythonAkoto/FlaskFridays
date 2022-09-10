from flask import Flask


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
app.config["TRACK_MODIFICATIONS"] = True

# user interface
import trusthouse.routes.welcome_screen
import trusthouse.routes.homepage
import trusthouse.routes.create_review
import trusthouse.routes.display_reviews
import trusthouse.routes.display_locations
import trusthouse.routes.filter_ratings
import trusthouse.routes.filter_door
import trusthouse.routes.filter_street
import trusthouse.routes.filter_location
import trusthouse.routes.filterpostcode
import trusthouse.routes.trust_map
import trusthouse.routes.upload_address
# backend api