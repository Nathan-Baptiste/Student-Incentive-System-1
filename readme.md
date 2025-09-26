## 816039236 - COMP 3613 Assignment 1 ##
## STUDENT INCENTIVE SYSTEM ##


# SETUP COMMANDS
1. Initialize the database:
    flask init

# STUDENT COMMANDS
1. Create a student:
    flask student create <first_name> <last_name> <email> <password>

2. List all students:
    flask student list

3. Request volunteer hours (needs to be confirmed by staff):
    flask student request_hours <student_id> <hours> <date> [description]
    *NOTE: date format: YYYY-MM-DD. The description is optional.*

4. List student's volunteer hours:
    flask student list_hours <student_id>

5. List student's accolades:
    flask student list_accolades <student_id>


# STAFF COMMANDS
1. Create a staff member:
    flask staff create <first_name> <last_name> <email> <password>

2. List all staff members:
    flask staff list

3. Staff logs volunteer hours for a student:
    flask staff log_hours <student_id> <staff_id> <hours> <date> [description]
    *NOTE: date format: YYYY-MM-DD. The description is optional.*

4. Confirm or reject a student's requested hours:
    flask staff confirm_hours <hours_id> <status> <staff_id>
    *NOTE: status can be: PENDING, CONFIRMED or REJECTED*

5. List a student's volunteer hours:
    flask staff list_hours <student_id>


# LEADERBOARD COMMANDS
1. Show leaderboard:
    flask leaderboard show [limit]
    *NOTE: limit (optional, default 20) sets how many entries to show.*