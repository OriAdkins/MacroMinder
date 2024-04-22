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
│ └── ViewUserDashboard.html
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
