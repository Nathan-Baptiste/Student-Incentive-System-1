from App.models import Accolade, Student
from App.database import db

def list_accolades_for_student(student_id):
    s = db.session.get(Student, student_id)
    if not s:
        return []
    return [a.get_json() for a in s.accolades]

def award_accolade(student_id, milestone_hours):
    return Accolade.awardAccolade(student_id=student_id, milestone_hours=milestone_hours)
