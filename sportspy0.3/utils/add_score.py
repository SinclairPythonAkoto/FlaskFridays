from models.scores import Score
from ..extensions import app, db
from datetime import datetime


def add_new_score(student_score, student_notes, student):
    """
    Creates a new score, storing it into the Score db table.

    Returns the Score object after saving it.
    """
    with app.app_context():
        new_score = Score(
            Score = student_score,
            notes = student_notes.lower(),
            date = datetime.now(),
        )
        db.session.add(new_score)
        db.session.commit()
    return new_score