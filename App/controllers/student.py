from App.models import Student
from App.database import db

def create_student(first_name, last_name, email, password):
    s = Student(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(s)
    db.session.commit()
    return s

def get_student(student_id):
    return db.session.get(Student, student_id)

def get_student_by_email(email):
    result = db.session.execute(db.select(Student).filter_by(email=email))
    return result.scalar_one_or_none()

def list_students():
    return db.session.scalars(db.select(Student)).all()

def student_json_list():
    return [s.get_json() for s in list_students()]

def view_student_accolades(student_id):
    s = get_student(student_id)
    if not s:
        return None
    return s.viewAccolades()
