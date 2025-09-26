from datetime import date
from App.database import db
from sqlalchemy.orm import relationship
from App.models.accolade import Accolade
from App.models.volunteer_hours import VolunteerHours

class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    # relationships
    volunteer_hours = relationship("VolunteerHours", back_populates="student", cascade="all, delete-orphan")
    accolades = relationship("Accolade", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.student_id} {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_hours(self):
        confirmed = [vh.hours for vh in self.volunteer_hours if vh.status.name == 'CONFIRMED']
        return float(sum(confirmed)) if confirmed else 0.0

    def viewAccolades(self):
        return [a.get_json() for a in self.accolades]

    def viewTotalHours(self):
        return self.total_hours

    def get_json(self):
        return {
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'total_hours': self.total_hours
        }
