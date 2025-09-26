from datetime import date
from App.models import VolunteerHours, Student, Accolade
from App.models.status_enum import VolunteerStatus
from App.database import db

# Milestones for accolades
MILESTONES = [10, 25, 50]

def create_volunteer_hours(student_id, staff_id=None, hours: float = 0.0, date: date = None, description: str = ""):
    if date is None:
        date = date = date.today()
    vh = VolunteerHours(student_id=student_id, staff_id=staff_id, hours=hours, date=date, description=description, status=VolunteerStatus.PENDING)
    db.session.add(vh)
    db.session.commit()
    return vh

def get_volunteer_hours(hours_id):
    return db.session.get(VolunteerHours, hours_id)

def list_volunteer_hours_for_student(student_id):
    result = db.session.scalars(db.select(VolunteerHours).filter_by(student_id=student_id))
    return result.all()

def update_volunteer_status(hours_id, status, staff_id=None):
    """
    status: string or VolunteerStatus
    If status moves to CONFIRMED, check for accolades.
    """
    vh = get_volunteer_hours(hours_id)
    if not vh:
        return None
    if isinstance(status, str):
        status = VolunteerStatus[status]
    vh.updateStatus(status, staff_id)
    db.session.commit()

    if status.name == "CONFIRMED":
        student = db.session.get(Student, vh.student_id)
        if student:
            total = student.total_hours
            existing_milestones = {a.milestone_hours for a in student.accolades}
            for m in sorted(MILESTONES):
                if total >= m and m not in existing_milestones:
                    Accolade.awardAccolade(student_id=student.student_id, milestone_hours=m)
    return vh
