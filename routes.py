from flask import render_template, request, flash, session, redirect, url_for, jsonify
from app import app, db, bcrypt
from models import User, Habits

# Render login page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Login route
# changed to get post, because we need the intial get request - Ori Changes also reflected in html
@app.route('/signin', methods=['GET', 'POST'])
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
    return redirect(url_for('index'))  #redirect to home page

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


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('AdminDashboard.html')

@app.route('/lifecoach/dashboard')
def lifecoach_dashboard():
    return render_template('LifecoachDashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    userid = session.get('userid') #retrive userid from session; id of the logged in user
    habits = Habits.query.filter_by(user_id=userid).all()
    #load UserDashboard.html with habits
    return render_template('UserDashboard.html', habits=habits)

#route to render the addhabit page or add a habit
@app.route('/addhabit', methods=['POST','GET'])
def addHabit():
    if request.method == 'POST':
        description = request.form.get('habitdesc')
        userid = session.get('userid')  # Retrieve userid from session
        role = session.get('role')  # Retrieve role from session

        if userid:
            existingHabit = Habits.query.filter_by(user_id=userid, habit_description=description).first()
            if existingHabit is None:
                newHabit = Habits(user_id=userid, habit_description=description)
                db.session.add(newHabit)
                db.session.commit()
                return jsonify({'success': True})  # Return success response
            else:
                return jsonify({'success': False, 'message': 'This habit already exists'})  # Return error response
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to add a habit.'})  # Return error response