# COP4521_Project

## Project Overview
MacroMinder - A Web App to track your macros and habits through the week!

## File Listing
```
├── templates/
│ └── AdminDashboard.html
│ └── LifecoachDashboard.html
│ └── LoginPage.html
│ └── RegisterPage.html
│ └── UserDashboard.html
├── services/
│ └── CompletionLogService.py
│ └── HabitService.py
│ └── TimeService.py
│ └── UserService.py
├── static/
│ └── css/
│     └── dashboard.css
│     └── LoginPage.css
│ └── js/
│     └── dashboard.js
│     └── script.js
├── app.py
├── models.py
├── routes.py
├── readme.md
```

### List of Implemented Features

#### User Features

Users have full CRUD functionality for Habits, being able to view a list of their daily habits while being able to edit and delete them as they wish.\
Users can also input Macro Data, and are limited to one input per day, however any subsequent inputs will edit the submission for that day to reflect the new input.\
Macro data is reflected in the Plotly line graph, which updates to show the users weight over the date. \
Users also have access to a list of the current signed-up lifecoaches, where they can choose a lifecoach to 'pair to'.

#### Lifecoach Features

Lifecoaches have access to any paired Users dashboard, allowing them to add macro and habits for them.\
Lifecoaches can be paired to many users, but users can only have one lifecoach.

#### Admin Features

Admins are able to see a comprehensive list of all users and their role.\
Admins are able to edit users roles, usernames, and passwords if necessary.\
Admins can also create new users from their dashboard.

## How to Run

### Creating the DB

# On Windows Machines
First, install MySQL Server and Shell. These will allow you to create a local database to interact with the program.
Using MySql Shell, connect to a MySql server, and create the DB.

# On Ubuntu (Linux)
Follow this tutorial until you can login to an instance of MySql, then create the DB.
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

### First Steps

First Steps\
  Ensure you have an SQL Server instance running\
  Pull up the project in a terminal\
  Navigate into the server folder\
  Install dependencies (Check dependencies section) using
  - ```pip install Flask Flask-SQLAlchemy Flask-Bcrypt Flask-SocketIO setuptools numpy plotly pandas```
  type ```flask run``` and the development server will deploy to your localhost http://127.0.0.1:5000

  Enter mysql mysql -u root -p (enter password for root or your username input)
  Once in an instance of mysql, create a database, and run these commands to make the neccessary tables: \
CREATE DATABASE macrominder; \
CREATE TABLE User ( \
    id INT AUTO_INCREMENT PRIMARY KEY, \
    username VARCHAR(80) UNIQUE NOT NULL, \
    password VARCHAR(80) NOT NULL, \
    role VARCHAR(80) NOT NULL \
); \
CREATE TABLE Habits ( \
    habit_id INT, \
    user_id INT NOT NULL, \
    habit_description VARCHAR(255) NOT NULL, \
    is_completed BOOLEAN DEFAULT FALSE, \
    date DATE NOT NULL, \ 
    PRIMARY KEY (habit_id, date), \
    FOREIGN KEY (user_id) REFERENCES User(id) \
); \
CREATE TABLE CompletionLog ( \
    tracking_id INT PRIMARY KEY AUTO_INCREMENT, \
    user_id INT NOT NULL, \
    date DATE NOT NULL, \
    protein INT DEFAULT 0, \
    calories INT DEFAULT 0, \
    tasks_completed INT DEFAULT 0, \
    weightlbs DECIMAL (5,2) DEFAULT 150.00, \
    FOREIGN KEY (user_id) REFERENCES User(id) \
); 

CREATE TABLE CoachingGroups ( \
    life_coach_id INT NOT NULL, \
    user_id INT NOT NULL, \
    PRIMARY KEY (life_coach_id, user_id), \
    FOREIGN KEY (life_coach_id) REFERENCES User(id), \
    FOREIGN KEY (user_id) REFERENCES User(id) \
); 




### If you are having errors, here are some commands that might help - Ori
#### Dependencies to install
``` sudo pip install mysqlclient ```\
``` sudo apt install mysql-server ```\
``` pip install pymysql ```\
``` pip install mysql-connector ```\
``` pip install mysql-connector-python-rf ```\
``` pip install mysql-connector-python ```\
``` pip install Werkzeug ```\
``` sudo apt-get update ```\
``` sudo apt-get install python-mysqldb ```\
``` sudo apt-get install libmysqlclient-dev ```\
``` pip install Flask-SQLAlchemy ```\
``` pip install Flask-Bcrypt ```\
``` pip install Flask-SocketIO ```\
``` pip install --upgrade pip ```\
``` pip install --upgrade setuptools ```\
``` pip install --upgrade Flask ```\
``` pip install --upgrade Werkzeug ```\
``` sudo apt-get install build-essential ```\
``` pip install mysqlclient ```

Please note that some of these may not be required, but when troubleshooting we found that after running these, the actual server decided to open.

## Group Members
- Ori Adkins (gda20b)
- Liam Salem (lcs21j)
- Ryan Rowe (rfr21)
- Sam Zinn (sjz20g)
