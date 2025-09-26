from App.models import Staff
from App.database import db

def create_staff(first_name, last_name, email, password):
    s = Staff(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(s)
    db.session.commit()
    return s

def get_staff(staff_id):
    return db.session.get(Staff, staff_id)

def get_staff_by_email(email):
    result = db.session.execute(db.select(Staff).filter_by(email=email))
    return result.scalar_one_or_none()

def list_staff():
    return db.session.scalars(db.select(Staff)).all()
