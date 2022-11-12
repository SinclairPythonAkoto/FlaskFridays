from models.students import Student
from ..extensions import app, db


def create_new_student(student_name, usr_project):
    """
    Creates a new student, storing it in the Student db table.

    Returns the Student object after saving it.
    """
    with app.app_context():
        new_student = Student(
            name = student_name,
            project = usr_project,
        )
        db.session.add(new_student)
        db.session.commit()
    return new_student