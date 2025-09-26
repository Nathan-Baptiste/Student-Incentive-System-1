from datetime import date
from App.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Accolade(db.Model):
    __tablename__ = 'accolades'

    accolade_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('students.student_id'), nullable=False)
    award_date = db.Column(db.Date, nullable=False, default=date.today)
    milestone_hours = db.Column(db.Integer, nullable=False)

    student = relationship("Student", back_populates="accolades")

    def __repr__(self):
        return f"<Accolade {self.accolade_id} student={self.student_id} milestone={self.milestone_hours}>"

    def get_json(self):
        return {
            'accolade_id': self.accolade_id,
            'student_id': self.student_id,
            'award_date': self.award_date.isoformat() if self.award_date else None,
            'milestone_hours': self.milestone_hours
        }

    @classmethod
    def awardAccolade(cls, student_id: int, milestone_hours: int):
        from App.database import db
        new = cls(student_id=student_id, milestone_hours=milestone_hours)
        db.session.add(new)
        db.session.commit()
        return new
