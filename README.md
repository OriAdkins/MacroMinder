# MacroMinder

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
│ └── UserView.html
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

#### On Windows Machines
First, install MySQL Server and Shell. These will allow you to create a local database to interact with the program.
Using MySql Shell, connect to a MySql server, and create the DB.

#### On Ubuntu (Linux)
Follow this tutorial until you can login to an instance of MySql, then create the DB.
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

## First Steps

First Steps\
  Ensure you have an SQL Server instance running\
  Pull up the project in a terminal\
  Navigate into the server folder\
  Install dependencies (Check dependencies section) using
  - ```python3 -m pip install Flask Flask-SQLAlchemy Flask-Bcrypt Flask-SocketIO setuptools numpy plotly pandas```
  type ```flask run``` and the development server will deploy to your localhost http://127.0.0.1:5000 \

  In the app.py, edit the following line: app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:monkeyinhospital@localhost/users' \
  And instead replace root with who you are running the vm as, and replace monkeyinhospital with your password, and users with your database name made in the last step ie:\
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://"user":"password"@localhost/"databasename"' \
  
 
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




#### If you are having errors, here are some commands that might help - Ori
### Dependencies to install
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
- Ori Adkins 
- Liam Salem 
- Ryan Rowe 
- Sam Zinn 

## Distribution Plan
This step-by-step report outlines the hypothetical process of deploying our Flask application, which currently uses SQLAlchemy on localhost, to the cloud. The deployment process involves containerizing the application and then deploying it to a cloud service. Containerizing our Flask application and deploying it to the cloud would have made our development process more efficient. It ensures an application runs consistently across all environments, simplifying the process of managing dependencies. It also allows us to easily scale our application to handle more traffic as needed.

### Steps
#### Containerize application
1. Create dockerfile
   1. First we add an official python image into the dockerfile
   2. Set working directory to /app
   3. Copy our application into directory
   4. Install requirements/dependencies (run pip install for all of them)
   5. Expose port 5000
   6. Set flask app environment to app.py
   7. Run the app with host as 0.0.0.0 so anyone can connect
2. Build docker image (docker build) and test it by running it locally (docker run)
   1. Then, we would look to push this to a docker registry like Docker Hub or Amazon Elastic Container Registry
   2. Note the URL and Share it
#### Choose cloud service for deployment
1. We would choose Azure Kubernetes Service (AKS)
#### Prepare for development
1. Push Docker image to a container registry. For our container registry, we will choose Azure Container Registry (ACR) since it is specifically designed to work with Azure services like AKS, simplifying container management and deployment processes.
2. Configure container service (ACR) in the cloud platform (AKS): create an ACR, authenticate Docker to ACR, tag the Docker image, and push the image
#### Deploy the application
1. Create deployment and service configurations: for AKS, we have to create a YAML config file, which defines deployment specifications for Kubernetes-based services.
2. Use a CLI tool to deploy: we chose kubectl, the standard Kubernetes command-line tool, since we are using a kubernetes-based service.
3. Monitor and scale application’s performance on Azure
#### Set up a CI/CD pipeline to automate the testing and deployment of your application whenever changes are made to the code: We will use Azure DevOps Services because it includes Azure pipelines. Steps below:
1. Create a project
2. Setup build pipeline: Create a new pipeline and connect the source code repository to it. Configure the pipeline choosing the "Docker: Build and push an image to Azure Container Registry" template since this uses the tools we are using to deploy the application.
   1. Purpose: Automates the testing and building of code every time a commit is made in a repo
3. Set up release pipeline 
   1. Purpose: Manages the deployment of software to different environments, ensuring that the software can be reliably released at any time with minimal manual intervention. starts where the build pipeline ends, taking the built artifacts and deploying them in the required environments
#### In order for users to access our database without the need to set up their own, we would need to persist our database and allow users to connect to it. For a client-server database system, we are most familiar with MySQL so would probably follow through.
1. We would need to set up a database server. I have used Microsoft Azure before so that or Digital Ocean looks appealing too. 
2. We would need to migrate our data that we have now, the tables and information we would like to carry over.
3. To handle database authentication and security, we would need to set up users with administrator roles. We would need to set up SSL/TLS and access control mechanisms. 
