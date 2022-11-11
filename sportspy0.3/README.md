# Sports Desktop App #

This is a desktop app built with Flask and Flask-Web GUI.

The aim of this app is to allow sports coahes to create their own training sessions and analyze the data over a 6 week period.

### Installation ###
You will need to install the following:
- Flask
- Flask SQL-Alchemy
- Flask Web GUI
- Datetime 
```
pip install Flask
pip install Flask-SQLAlchemy
pip install flaskwebgui
pip install datetime
```

This will be a simple implementtion of how a user would create a new project full of students, and then display the different projects created.

After that I will expand on the project by creating capablities for the user to upload data into the tables created, and implement different ways to view the information.


# Sports Desktop App (sportsPY) 0.2 #

In this version of the app, the Flask app will be created using class **MethodViews**.  By doing this I will create a modular Flask app that will help me to expand the project as it grows.  Instead of haing a `main.py` file, all the routes (pages) of the desktop is created in a class and imported into the `__init__.py` file.  The models haven't changed, they are now in a separate folder.  With everything compartmenalised it makes it easier to maintain the modular app.


# sportsPY 0.3 #

In this version of the app I will attempt the same using **Flask Blueprint**.