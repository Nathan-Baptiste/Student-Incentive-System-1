from App.database import db
from sqlalchemy.orm import relationship
from App.models.volunteer_hours import VolunteerHours

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    volunteer_hours = relationship("VolunteerHours", back_populates="staff", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Staff {self.staff_id} {self.first_name} {self.last_name}>"

    def get_json(self):
        return {
            'staff_id': self.staff_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def logHours(self, student_id, hours, date_performed, description=""):
        from App.controllers.volunteer_hours import create_volunteer_hours
        return create_volunteer_hours(student_id=student_id, staff_id=self.staff_id, hours=hours, date=date_performed, description=description)

    def confirmHours(self, hours_id, status):
        from App.controllers.volunteer_hours import update_volunteer_status
        return update_volunteer_status(hours_id=hours_id, status=status, staff_id=self.staff_id)
