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
First Steps\
  Ensure you have an SQL Server instance running\
  Pull up the project in a terminal\
  Navigate into the server folder\
  Install dependencies (Check dependencies section) using
  - ```pip install Flask Flask-SQLAlchemy Flask-Bcrypt Flask-SocketIO setuptools numpy plotly pandas```
  type ```flask run``` and the development server will deploy to your localhost http://127.0.0.1:5000

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
