# Projekt-OSPR
Projekt za OSPR
#TODO
- []Cpanel - py flask, html
    - []console
    - []analytics
    - []database
    - []user system
    - []settings
    - []cpanel
    - []user settings
    - []backup
- [x]Home Page - html
- []Blog - html
    - [x]about - html
    - []TOS - html
    - [x]PP - html
- [x]Error - html
- [x]Login - flask login
    - Login/Register Website - FireBase, html, py
- []Payment System - flask PayPal
- [x]DataBase - firebase
    - [x]connection
    - [x]user's info
    - [x]user's general info
    - []Google Analytics
- [x]Plans site - html
- []currency acquiring system - firebase, py

  Addon:
  - []TailWind
  - []Bootstrap
  - []DarkMode
  - [x]1 File for primary settings - css
  - []SQL - Database - Data stealing
  - []Mini games - loading screens, coins collecting




Resources:
- https://firebase.google.com/ - database
- https://github.com/Jonontop/Projekt-OSPR
- https://flask.palletsprojects.com/en/stable/api/ - flask
- https://github.com/pallets-eco/flask-wtf - data tenement
- https://github.com/maxcountryman/flask-login - login
- https://medium.com/@andrii.gorshunov/paypal-flask-integration-python-2022-1c012322801d - paypal integration


# Structure:

OSPR-projekt/
- │
- ├── flaskr/
- │   ├── __init__.py      # Initialize the Flask app and bring everything together
- │   ├── routes.py        # Define the routes in this file
- │   ├── models.py        # Define the database models
- │   ├── auth.py          # Define the forms for user input
- │   ├── database.py      # Database connection and setup
- │   ├── docker.py        # Google Analytics integration
- │   ├── static/          # Static files (CSS, JS, etc.)
- │   │   └── css/         # Stylesheets
t
- │   │   └── js/          # JavaScript
- │   └── templates/       # HTML templates
- │       ├── index.html   # Home page
- │       ├── base.html    # Nav Bar
- │       ├── errors.html  # Dynamic error page
- │       ├── auth/        # Authentication templates
- │       │   └── login.html
- │       │   └── forgot_password.html
- │       ├── blog/        # Blog-related templates
- │       │   ├── about.html
- │       │   ├── TOS.html
- │       │   └── PP.html
- │       ├── cpanel/      # Control panel templates
- │       │   ├── console.html
- │       │   ├── analytics.html
- │       │   ├── database.html
- │       │   ├── user_system.html
- │       │   ├── settings.html
- │       │   └── cpanel.html
- │       ├── payment/      # Payment-related templates
- │       │   ├── payment.html
- │       │   └── plans.html
- ├── config.py            # Configuration settings (e.g., app settings, database)
- ├── run.py               # To run the application
- ├── venv/                # Virtual environment
- └── requirements.txt     # List of dependencies
