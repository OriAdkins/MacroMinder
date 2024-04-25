from flask import render_template, request, flash, session, redirect, url_for, jsonify
from app import app, db, bcrypt
from models import User, Habits, CompletionLog, CoachingGroups
from services.UserService import UserService
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService
from services.TimeService import TimeService
from services.CoachingService import CoachingService
from services.GraphService import GraphService
from datetime import date, datetime
import pandas as pd
import plotly.graph_objects as go

# route for login, it gets the username and password to verify the user
# this route sets up all session id's and directs the user to the correct dashboard
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existingUser = User.query.filter_by(username=username).first()

        if existingUser and bcrypt.check_password_hash(existingUser.password, password):
            session['username'] = existingUser.username
            session['userid'] = existingUser.id 
            session['role'] = existingUser.role
            session['current_date'] = date.today()

            if existingUser.role == 'Admin':
                return redirect(url_for('admin_dashboard'))  
            elif existingUser.role == 'LifeCoach':
                return redirect(url_for('lifecoach_dashboard'))  
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('LoginPage.html')

#route to log out of current account
#Explaining the use of session here, it is a feature provided by flask that
#essentially saves the 'current' users information to persist through multiple requests
@app.route('/signout', methods=['POST','GET'])
def logout():
    session.clear()  #remove all items from a session
    return redirect(url_for('login'))  #redirect to home page

# Route to render registration page
@app.route('/gotoregister', methods=['POST','GET'])
def goToRegister():
    return render_template('RegisterPage.html')

# this route obtains the information to build a user, calls UserService to create a user
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    #This calls the service for create user
    newUser = UserService.create_user(username, password, role)

    db.session.add(newUser)
    db.session.commit()
    return render_template('LoginPage.html')

# ------------------------------ ADMIN ROUTES --------------------------------------------

#the admin dashboard, obtains a full list of users using the UserService function
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    users = UserService.list_users()

    return render_template('AdminDashboard.html', users=users)

#Admin functionality of the delete portion of crud, new simplified version to make things simpler.
# this route uses multiple backend Services to delete a user, and all associated records in the db
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    HabitService.delete_all_user_habits(user_id)
    
    CompletionLogService.delete_all_user_completion_logs(user_id)

    CoachingService.delete_link(user_id)
    
    success = UserService.delete_user(user_id)
    
    return redirect(url_for('admin_dashboard'))

#Route takes in information from html of the new username,role,and password
#passes that information to the update user UserService funtion
@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    new_username = request.form.get('username')
    new_role = request.form.get('role')
    new_password = request.form.get('password')
    
    UserService.update_user(user_id, new_username, new_password, new_role)

    return redirect(url_for('admin_dashboard'))


#route for admin page that allows them to create users. 
#same as edit, calls create user 
@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    newUser = UserService.create_user(username, password, role)

    return redirect(url_for('admin_dashboard'))

# ---------------------------- USER ROUTES ----------------------------------------------

#the main user dashboard, calls various service layer functions to obtain all required information
#HabitService prints the habits for the session date, GraphService prints the graph corresponding
#UserService prints the lifecoach and Coaching groups checks for any paired groups.
@app.route('/user/dashboard')
def user_dashboard():
    userid = session.get('userid')
    username = session.get('username')
    session_date = session.get('current_date')
    #we have to use this to get the session date in a format the db can read
    current_date = TimeService.parse_session_date(session_date)

    life_coaches = UserService.get_life_coaches()
    connected_coach = None
    for coach in life_coaches:
        coaching_group = CoachingGroups.query.filter_by(user_id=userid, life_coach_id=coach.id).first()
        if coaching_group:
            connected_coach = coach
            break 

    #use graphservice to create the 2 graphs printed on the dashboard
    graph_html = GraphService.generate_habit_progress_graph(current_date, userid)
    macros_html = GraphService.generate_weight_over_time_graph(userid)

    habits = HabitService.list_habits(userid, current_date) #add date parameter

    return render_template('UserDashboard.html', habits=habits, current_date=current_date, username=username, life_coaches=life_coaches, connected_coach=connected_coach, graph_html=graph_html,
                           macros_html=macros_html)

#A route to set a coach, called when a user clicks on an available lifecoach in the dashboard
#uses Userservice to link a lifecoach and user in the CoachingGroups database table
@app.route('/set_coach/<int:life_coach_id>', methods=['POST'])
def set_coach(life_coach_id):
    print("Set coach route triggered")
    if session.get('role') != 'User':
        return redirect(url_for('login'))
    user_id = session.get('userid')

    success = UserService.link_user_and_coach(user_id, life_coach_id)
    if success:
        flash('Coach added successfully')
    else:
        flash('Failed to add coach')

    return redirect(url_for('user_dashboard'))

#route to render the addhabit page or add a habit
#called when a user clicks 'add' for a habit, takes the habit description and uses it to create a new habit for that date
@app.route('/addhabit', methods=['POST','GET'])
def addHabit():
    if request.method == 'POST':
        description = request.form.get('habitdesc')
        userid = session.get('userid') 
        current_date = session.get('current_date')
        current_date = TimeService.parse_session_date(current_date)

        if userid:
            success, response = HabitService.add_habit(userid, description, current_date)
            if success:
                return jsonify({'success': True, 'habit_id': response})
            else:
                return jsonify({'success': False, 'message': response})
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to add a habit.'})

#called when a checkbox is clicked, sets the database variable is_completed to true or false
@app.route('/checkbox', methods=['POST'])
def checkBox():
    habit_id = request.form.get('habit_id')
    current_date = session.get('current_date')
    current_date = TimeService.parse_session_date(current_date)
    completed = request.form.get('completed')=='True'
    habit = HabitService.get_habit(habit_id)
    if habit:
        HabitService.mark_completed(habit, completed)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})

#called when a user clicks edit habit, queries for the new description and edits the desired habit with HabitService
@app.route('/edithabit', methods=['POST'])
def editHabit():
    habit_id = request.form.get('habit_id')
    new_description = request.form.get('new_description')

    success = HabitService.edit_habit(habit_id, new_description)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})

#called when a user clicks delete habit, passes info to HabitService
@app.route('/deletehabit', methods=['POST'])
def deleteHabit():
    habit_id = request.form.get('habit_id')
    current_date = session.get('current_date')
    current_date = TimeService.parse_session_date(current_date)

    success = HabitService.delete_habit(habit_id, current_date)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})
    
#called when a user submits macro information, passes information to CompletionLogService
@app.route('/addmacros', methods=['POST'])
def add_macros():
    # Add macro to the database
    userid = session.get('userid')
    data = request.get_json()
    protein = data['protein']
    calories = data['calories']
    weightlbs = data['weightlbs']
    current_date = session.get('current_date')
    current_date = TimeService.parse_session_date(current_date)

    new_macro = CompletionLogService.add_completion_log(userid, current_date, protein, calories, 0, weightlbs)
  
    return jsonify({"success": True})

# ----------------------- LIFECOACH ROUTES ---------------------------------------

#the main lifecoach dashbaors, uses Coachingservice to print out all paired users
@app.route('/lifecoach/dashboard')
def lifecoach_dashboard():
    username = session.get('username')
    # Check lifecoach role
    if session.get('role') != 'LifeCoach':
        return redirect(url_for('login'))

    # Get the lifecoach's ID from the session
    lifecoach_id = session.get('userid')

    # Fetch paired users for the lifecoach
    paired_users = CoachingService.get_paired_users(lifecoach_id)

    # Render the lifecoach dashboard template with paired users
    return render_template('LifecoachDashboard.html', paired_users=paired_users, username=username)

#the view of the users dashboard from a lifecoach view, prints everything a user might see from userdashboard
#everything there applies here.
@app.route('/viewuser/<int:user_id>', methods=['GET'])
def view_user(user_id):
    # Check if the user is logged in
    #if 'userid' not in session:
    #    return redirect(url_for('login'))
    # Retrieve the user from the database
    user = User.query.get(user_id)
    user_username = user.username
    session_date = session.get('current_date')
    current_date = TimeService.parse_session_date(session_date)
    
    if not user:
        flash('User not found.')
        return redirect(url_for('lifecoach_dashboard'))
    
    habits = HabitService.list_habits(user_id, current_date)
    
    graph_html = GraphService.generate_habit_progress_graph(current_date, user_id)

    # Generate weight over time graph HTML
    macros_html = GraphService.generate_weight_over_time_graph(user_id)

    # Render the UserView.html template with the user's information
    return render_template('UserView.html', user=user, user_id=user_id, habits=habits, current_date=current_date, user_username=user_username, graph_html=graph_html, macros_html=macros_html)

#Lifecoaches version of add habit, gets the users id to add the habit through HabitService
@app.route('/coachAddHabit', methods=['POST'])
def coachAddHabit():
    if request.method == 'POST':
        data = request.json  # Parse JSON data from request
        description = data.get('habitdesc')
        user_id = request.json.get('user_id')
        current_date = session.get('current_date')
        current_date = TimeService.parse_session_date(current_date)

        if user_id:
            success, response = HabitService.add_habit(user_id, description, current_date)
            if success:
                return jsonify({'success': True, 'habit_id': response})
            else:
                return jsonify({'success': False, 'message': response})
        else:
            return jsonify({'success': False, 'message': 'User ID not provided.'})

#coaches log macros, essentially the same as users but takes in the users ID so that it is added for them not the coach
@app.route('/coach/logmacros', methods=['POST'])
def coach_log_macros():
    user_id = request.json.get('user_id')
    data = request.get_json()
    protein = data['protein']
    calories = data['calories']
    weightlbs = data['weightlbs']
    current_date = TimeService.parse_session_date(data['date'])

    new_macro = CompletionLogService.add_completion_log(user_id, current_date, protein, calories, 0, weightlbs)
  
    return jsonify({"success": True})



        
#sets the session id to the next date, using TimeService
@app.route('/nextday', methods=['POST'])
def next_day():
    TimeService.set_next_date()
    return jsonify({'success': True})

#sets the session ID to the previous date, using TimeService
@app.route('/prevday', methods=['POST'])
def prev_day():
    TimeService.set_previous_date()
    return jsonify({'success': True})