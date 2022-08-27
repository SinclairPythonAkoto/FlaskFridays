# Trust House 0.2 #

#### Required Installations ####
These will be installed in my *virual environment*.
- `pip install Flask`
- `pip install flask_sqlalchemy`
- `pip install datetime`

#### Create Database ####
We can automate the creation of the database by applying `db.create_all()` when we start the Flask app.

For this version of the web app I will create the database manually and then create a deafault entry.
***This process will be automated later.***

*Open Python in project directory.*
```
from datetime import datetime
from main import db, Building, Review

db.create_all()

default_address = Building(
    door_num='60',
    street='kingsly street',
    location='London'
    postcode='e14 2xb'
)
db.session.add(default_address)
db.session.commit()

default_review = Review(
    rating=3,
    review='Your review goes here...',
    reviewed_by='tenant',
    date=datetime.now(),
    building=default_address,
)
db.session.add(default_review)
db.session.commit()
```
