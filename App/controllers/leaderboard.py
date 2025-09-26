from App.models import Student
from App.database import db

def compute_leaderboard(limit=50):
    students = db.session.scalars(db.select(Student)).all()
    rows = []
    for s in students:
        rows.append({
            'student_id': s.student_id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'total_hours': s.total_hours
        })
    rows.sort(key=lambda r: r['total_hours'], reverse=True)
    rank = 1
    last_hours = None
    for i, r in enumerate(rows):
        if last_hours is None:
            r['rank'] = rank
            last_hours = r['total_hours']
        else:
            if r['total_hours'] < last_hours:
                rank = i + 1
            r['rank'] = rank
            last_hours = r['total_hours']
    return rows[:limit]