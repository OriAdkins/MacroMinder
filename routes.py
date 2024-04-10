from flask import render_template, request, flash, session, redirect, url_for
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
        userid = session.get('userid')  #retrieve userid from session
        role = session.get('role') #retrieve role from session
        #if the user is logged in, check if the habit exists 
        if userid:
            existingHabit = Habits.query.filter_by(user_id=userid, habit_description=description).first()
            #if it does not exist, add newHabit to the database. otherwise, notify user the habit exists
            if existingHabit is None:
                newHabit = Habits(user_id=userid, habit_description=description)
                db.session.add(newHabit)
                db.session.commit()
                if role=='User':
                    return redirect(url_for('user_dashboard'))  #back to the dashboard
                elif role=='Admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('lifecoach_dashboard'))
            else:
                flash('This habit already exists')
        else:
            flash('You must be logged in to add a habit.')


    # Render the AddHabit page (GET request or failed login)
    return render_template('AddHabit.html')