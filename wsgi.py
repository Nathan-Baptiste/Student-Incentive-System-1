import click, pytest, sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="flask_admin.contrib")

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.database import db, get_migrate
from App.controllers.student import (create_student, list_students, student_json_list)
from App.controllers.staff import (create_staff, list_staff)
from App.controllers.volunteer_hours import (create_volunteer_hours, list_volunteer_hours_for_student, update_volunteer_status, get_volunteer_hours)
from App.controllers.accolade import (award_accolade, list_accolades_for_student)
from App.controllers.leaderboard import (compute_leaderboard)
from App.controllers import (create_user, get_all_users, get_all_users_json, initialize)  # keep original user functions

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
STUDENT COMMANDS
'''
student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("create", help="Create a student")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("email")
@click.argument("password")
def create_student_command(first_name, last_name, email, password):
    s = create_student(first_name, last_name, email, password)
    print("Created:", s.get_json())

@student_cli.command("list", help="List students")
def list_students_command():
    for s in list_students():
        print(s.get_json())

@student_cli.command("request_hours", help="Student requests volunteer hours")
@click.argument("student_id", type=int)
@click.argument("hours", type=float)
@click.argument("date")
@click.argument("description", default="", required=False)
def request_hours_command(student_id, hours, date, description):
    import datetime
    d = datetime.date.fromisoformat(date)
    vh = create_volunteer_hours(student_id=student_id, hours=hours, date=d, description=description)
    print("Requested:", vh.get_json())

@student_cli.command("list_hours", help="List a student's volunteer hours")
@click.argument("student_id", type=int)
def list_hours_command(student_id):
    vhs = list_volunteer_hours_for_student(student_id)
    for v in vhs:
        print(v.get_json())

@student_cli.command("list_accolades", help="List accolades for a student")
@click.argument("student_id", type=int)
def list_accolades_command(student_id):
    for a in list_accolades_for_student(student_id):
        print(a)

app.cli.add_command(student_cli)



'''
STAFF COMMANDS
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Create a staff member")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("email")
@click.argument("password")
def create_staff_command(first_name, last_name, email, password):
    s = create_staff(first_name, last_name, email, password)
    print("Created staff:", s.get_json())

@staff_cli.command("list", help="List staff")
def list_staff_command():
    for s in list_staff():
        print(s.get_json())

@staff_cli.command("log_hours", help="Staff logs hours directly (auto-confirmed)")
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("hours", type=float)
@click.argument("date")
@click.argument("description", default="", required=False)
def log_hours_command(student_id, staff_id, hours, date, description):
    import datetime
    from App.models.status_enum import VolunteerStatus

    d = datetime.date.fromisoformat(date)
    vh = create_volunteer_hours(
        student_id=student_id,
        staff_id=staff_id,
        hours=hours,
        date=d,
        description=description,
    )
    # Immediately mark as CONFIRMED
    from App.controllers.volunteer_hours import update_volunteer_status
    vh = update_volunteer_status(hours_id=vh.hours_id, status=VolunteerStatus.CONFIRMED.name, staff_id=staff_id)

    print("Logged:", vh.get_json())

@staff_cli.command("confirm_hours", help="Confirm or reject a volunteer entry")
@click.argument("hours_id", type=int)
@click.argument("status")  # PENDING/CONFIRMED/REJECTED
@click.argument("staff_id", type=int)
def confirm_hours_command(hours_id, status, staff_id):
    vh = update_volunteer_status(hours_id=hours_id, status=status, staff_id=staff_id)
    if vh:
        print("Updated:", vh.get_json())
    else:
        print("Not found:", hours_id)

@staff_cli.command("list_hours", help="List volunteer hours for a student")
@click.argument("student_id", type=int)
def staff_list_hours(student_id):
    vhs = list_volunteer_hours_for_student(student_id)
    for v in vhs:
        print(v.get_json())

app.cli.add_command(staff_cli)



'''
LEADERBOARD COMMANDS
'''
lb_cli = AppGroup('leaderboard', help='Leaderboard commands')

@lb_cli.command("show", help="Show leaderboard")
@click.argument("limit", default=20, type=int)
def show_leaderboard(limit):
    rows = compute_leaderboard(limit=limit)
    for r in rows:
        print(r)

app.cli.add_command(lb_cli)