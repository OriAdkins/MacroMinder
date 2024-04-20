from flask import render_template, request, flash, session, redirect, url_for, jsonify
from app import app, db, bcrypt
from models import User, Habits, CompletionLog
from services.UserService import UserService, HabitService, CompletionLogService

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
            session['userid'] = existingUser.id 
            session['role'] = existingUser.role
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

    habits = HabitService.list_habits(userid)

    #load UserDashboard.html with habits
    return render_template('UserDashboard.html', habits=habits)


#route to render the addhabit page or add a habit
@app.route('/addhabit', methods=['POST','GET'])
def addHabit():
    if request.method == 'POST':
        description = request.form.get('habitdesc')
        userid = session.get('userid') 

        if userid:
            success, response = HabitService.add_habit(userid, description)
            if success:
                return jsonify({'success': True, 'habit_id': response})
            else:
                return jsonify({'success': False, 'message': response})
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to add a habit.'})
                
@app.route('/checkbox', methods=['POST'])
def checkBox():
    habit_id = request.form.get('habit_id')
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

    success = HabitService.delete_habit(habit_id)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})