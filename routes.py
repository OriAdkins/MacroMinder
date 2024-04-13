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
            session['userid'] = existingUser.id  #store the user id in session
            session['role'] = existingUser.role #store the user role in session
            # Check user role and redirect accordingly
            print("User role:", existingUser.role)  # Debug print to check the user's role
            if existingUser.role == 'Admin':
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            elif existingUser.role == 'LifeCoach':
                return redirect(url_for('lifecoach_dashboard'))  # Redirect to lifecoach dashboard
            else:
                return redirect(url_for('user_dashboard'))   # Redirect to user dashboard
        else:
            flash('Invalid username or password')

    # Render the login page (GET request or failed login)
    return render_template('LoginPage.html')

#route to log out of current account
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

#route to delete a user, uses the user_id variable extracted from js
#get the user info, check if it exists, then delete it.
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if user:
        #query habits/logs table, only selecting with the specified user ID then delete them.
        Habits.query.filter_by(user_id=user_id).delete()
        CompletionLog.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User Deleted'})
    else:
        return jsonify({'success': False, 'message': 'User does not exist'}), 404



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
        role = session.get('role') 

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
        
                
@app.route('/logcompletion', methods=['POST'])
def logCompletion():
    userid = session.get('userid')
    habits = Habits.query.filter_by(user_id=userid).all()
    return render_template('UserDashboard.html', habits=habits)