from flask import render_template, request, flash, session, redirect, url_for, jsonify
from app import app, db, bcrypt
from models import User, Habits, CompletionLog
from services.UserService import UserService
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService
from services.TimeService import TimeService
from datetime import date, datetime

# Render login page

# Login route
# changed to get post, because we need the intial get request - Ori Changes also reflected in html
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existingUser = User.query.filter_by(username=username).first()

        if existingUser and bcrypt.check_password_hash(existingUser.password, password):
            #store the user id in current session
            session['username'] = existingUser.username
            session['userid'] = existingUser.id 
            session['role'] = existingUser.role
            session['current_date'] = date.today()

            # get.session.id check the user!
            # check time session['current_date'] = datetime.date.today()
            # call HabitService function that takes the userid and date
            # checkforexistinghabits(userid, date)
            # query db for prev day, add them to today (or call a function that does)
            # that would be added to the list of habits today which is already called by list_habits()




            #Check user role and redirect accordingly
            #print("User role:", existingUser.role)  # Debug print to check the user's role
            if existingUser.role == 'Admin':
                return redirect(url_for('admin_dashboard'))  
            elif existingUser.role == 'LifeCoach':
                return redirect(url_for('lifecoach_dashboard'))  
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')

    # Render the login page (GET request or failed login)
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

# Registration route
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

#error checking to see if someone is an admin (avoids attacks)
#also uses query to get all users, store in variable, and print them on the dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    users = UserService.list_users()
    #lifecoaches = User.query.filter_by(role='LifeCoach').all()

    return render_template('AdminDashboard.html', users=users)

#Admin functionality of the delete portion of crud, new simplified version to make things simpler.
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'Admin':
        # Redirect the user to the login page if they are not an admin
        return redirect(url_for('login'))
    
    #delete all related data first, then the user
    #utilizing service layer
    HabitService.delete_all_user_habits(user_id)
    
    CompletionLogService.delete_all_user_completion_logs(user_id)
    
    success = UserService.delete_user(user_id)
    
    # Redirect the user to the admin dashboard regardless of the outcome
    return redirect(url_for('admin_dashboard'))

#Route/function for processing the post request for editing a user
@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    #first check against the role (like the other admin functions)
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    new_username = request.form.get('username')
    new_role = request.form.get('role')
    new_password = request.form.get('password')
    
    UserService.update_user(user_id, new_username, new_password, new_role)

    return redirect(url_for('admin_dashboard'))


#route for admin page that allows them to create users.  
@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    #essentially the same as login, just only accessible from the admin dashboard
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    #This calls the service for create user
    newUser = UserService.create_user(username, password, role)
    #using the redirect here acts as a dummy 'refresh' though I think it is better to use Jsonify and JS to handle that.
    #also used in other admin functions
    return redirect(url_for('admin_dashboard'))

@app.route('/lifecoach/dashboard')
def lifecoach_dashboard():
    return render_template('LifecoachDashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    userid = session.get('userid') #retrive userid from session; id of the logged in user
    username = session.get('username')
    session_date = session.get('current_date')
    current_date = TimeService.parse_session_date(session_date)
    current_date_iso = current_date.isoformat()
    
    print("Type of session_date:", type(session_date))
    print("Type of session_date:", type(current_date))
    # formatted_date = current_date.strftime('%Y-%m-%d')
    # Handle case to copy habits over from previous date to current
    # (1) check current date, check for habits on day before. 
    # copy them over in habit service. 

    #current_date = datetime.date.today()

    #HabitService.get_habits_from_prev_days(userid, date)

    #LETS GOOOOOOO THIS WORKS
    #current_date = date(2024, 4, 22)

    habits = HabitService.list_habits(userid, current_date) #add date parameter

    #load UserDashboard.html with habits
    return render_template('UserDashboard.html', habits=habits, current_date=current_date_iso, username=username)


#route to render the addhabit page or add a habit
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
    
@app.route('/edithabit', methods=['POST'])
def editHabit():
    habit_id = request.form.get('habit_id')
    new_description = request.form.get('new_description')

    success = HabitService.edit_habit(habit_id, new_description)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})


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

    
@app.route('/lifecoach/viewuserdashboard/<int:user_id>')
def view_user_dashboard(user_id):
    if session.get('role') != 'LifeCoach':
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    user_username = user.username  #fetch user
    habits = HabitService.list_habits(user_id)

    return render_template('ViewUserDashboard.html', user=user, user_username=user_username, habits=habits)

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

@app.route('/editmacros', methods=['POST'])
def edit_macros():
        # Edit macro in the database
        userid = session.get('userid')
        data = request.get_json()
        macro_id = data['macro_id']
        protein = data['protein']
        calories = data['calories']
        weightlbs = data['weightlbs']
        date = data['date']

        success = CompletionLogService.edit_completion_log(macro_id, protein, calories, 0, weightlbs)
      
        if success:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Macro not found"})
        
@app.route('/nextday', methods=['POST'])
def next_day():
    TimeService.set_next_date()
    return jsonify({'success': True})

@app.route('/prevday', methods=['POST'])
def prev_day():
    TimeService.set_previous_date()
    return jsonify({'success': True})


#add two routes for going forward and back a date

#next and prev date button
#route next prev date button 
#session[current_date] = next/prev datetimetoday