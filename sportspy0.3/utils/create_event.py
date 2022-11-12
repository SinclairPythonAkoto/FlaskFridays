from models.projects import Project
from ..extensions import app, db
from datetime import datetime


def create_new_project(proj_name):
    """
    Creates a new project, storing it in the Project db table.

    Returns the Project object after saving it.
    """
    with app.app_context():
        new_project = Project(
            name = proj_name,
            date = datetime.now(),
        )
        db.session.add(new_project)
        db.session.commit()
    return new_project