from flask import render_template, request, flash, session, redirect, url_for, jsonify
from app import app, db, bcrypt
from models import User, Habits, CompletionLog

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
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    
    newUser = User(username=username, password=hashedPassword, role=role)

    db.session.add(newUser)
    db.session.commit()
    return render_template('LoginPage.html')

#error checking to see if someone is an admin (avoids attacks)
#also uses query to get all users, store in variable, and print them on the dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    users = User.query.all()
    #lifecoaches = User.query.filter_by(role='LifeCoach').all()

    return render_template('AdminDashboard.html', users=users)

#Admin functionality of the delete portion of crud, new simplified version to make things simpler.
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'Admin':
        #if they arent an admin and try to request this form (somehow) then redirect them to login
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if user:
        #filter by the user id, which essentially picks the user to delete, since they are unique
        Habits.query.filter_by(user_id=user_id).delete()
        CompletionLog.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin_dashboard'))

#Route/function for processing the post request for editing a user
@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    #first check against the role (like the other admin functions)
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if user:
        #this is essentially the same thing as register, but in a pop-up
        new_username = request.form.get('username')
        new_role = request.form.get('role')
        new_password = request.form.get('password')
        
        #this updates the username, then we commit after it updates
        if new_username:
            user.username = new_username
        if new_role:
            user.role = new_role
        if new_password:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password

        db.session.commit()

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
    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    
    newUser = User(username=username, password=hashedPassword, role=role)

    db.session.add(newUser)
    db.session.commit()
    #using the redirect here acts as a dummy 'refresh' though I think it is better to use Jsonify and JS to handle that.
    #also used in other admin functions
    return redirect(url_for('admin_dashboard'))

@app.route('/lifecoach/dashboard')
def lifecoach_dashboard():
    return render_template('LifecoachDashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    userid = session.get('userid') #retrive userid from session; id of the logged in user
    habits = Habits.query.filter_by(user_id=userid).all() #get habits and print
    #load UserDashboard.html with habits
    return render_template('UserDashboard.html', habits=habits)


#route to render the addhabit page or add a habit
@app.route('/addhabit', methods=['POST','GET'])
def addHabit():
    if request.method == 'POST':
        description = request.form.get('habitdesc')
        userid = session.get('userid') 

        if userid:
            existingHabit = Habits.query.filter_by(user_id=userid, habit_description=description).first()
            if existingHabit is None:
                newHabit = Habits(user_id=userid, habit_description=description)
                db.session.add(newHabit)
                db.session.commit()
                return jsonify({'success': True, 'habit_id': newHabit.habit_id})  # Return success response
            else:
                return jsonify({'success': False, 'message': 'This habit already exists'})  # Return error response
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to add a habit.'})  # Return error response
        
                
@app.route('/checkbox', methods=['POST'])
def checkBox():
    habit_id = request.form.get('habit_id')
    completed = request.form.get('completed')=='True'
    habit = Habits.query.get(habit_id)
    if habit:
        habit.is_completed = completed
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})
    
@app.route('/edithabit', methods=['POST'])
def editHabit():
    habit_id = request.form.get('habit_id')
    new_description = request.form.get('new_description')
    habit = Habits.query.get(habit_id)
    if habit:
        habit.habit_description = new_description
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})

@app.route('/deletehabit', methods=['POST'])
def deleteHabit():
    habit_id = request.form.get('habit_id')
    habit = Habits.query.get(habit_id)
    print("habit id: ", habit_id)
    if habit:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})