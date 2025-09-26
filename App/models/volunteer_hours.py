from datetime import date
from App.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from App.models.status_enum import VolunteerStatus

class VolunteerHours(db.Model):
    __tablename__ = 'volunteer_hours'

    hours_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('students.student_id'), nullable=False)
    staff_id = db.Column(db.Integer, ForeignKey('staff.staff_id'), nullable=True)
    hours = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.Enum(VolunteerStatus), default=VolunteerStatus.PENDING, nullable=False)
    description = db.Column(db.String(512), nullable=True)

    student = relationship("Student", back_populates="volunteer_hours")
    staff = relationship("Staff", back_populates="volunteer_hours")

    def __repr__(self):
        return f"<VolunteerHours {self.hours_id} student={self.student_id} hours={self.hours} status={self.status}>"

    def get_json(self):
        return {
            'hours_id': self.hours_id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'hours': float(self.hours),
            'date': self.date.isoformat() if self.date else None,
            'status': self.status.name if self.status else None,
            'description': self.description
        }

    def updateStatus(self, status, staff_id=None):
        if isinstance(status, str):
            status = VolunteerStatus[status]
        self.status = status
        if staff_id:
            self.staff_id = staff_id
