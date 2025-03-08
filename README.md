# Projekt-OSPR
Projekt za OSPR
#TODO
- []Cpanel - py flask, html
    - []console
    - []analitics
    - []database
    - []user system
    - []settings
    - []cpanel
- []Home Page - html
- []Blog - html
    - []about - html
    - []TOS - html
    - []PP - html
- []Error - html
    - []404 - html
- []Login - flask login
    - Login/Register Website - FireBase, html, py
- []Payment System - flask paypal
- []DataBase - firebase
    - [x]connection
    - []user's info
    - []user's general info
    - [x]Google Analitics
- []Plans site - html
- []currency acquering system - firebase, py




Resources:
- https://firebase.google.com/ - database
- https://github.com/Jonontop/Projekt-OSPR
- https://flask.palletsprojects.com/en/stable/api/ - flask
- https://github.com/pallets-eco/flask-wtf - data menegment
- https://github.com/maxcountryman/flask-login - login
- https://medium.com/@andrii.gorshunov/paypal-flask-integration-python-2022-1c012322801d - paypal integration


# Structure:

OSPR-projekt/
- │
- ├── flask/
- │   ├── __init__.py      # Initialize the Flask app and bring everything together
- │   ├── routes.py        # Define the routes in this file
- │   ├── auth/            # Authentication related views
- │   │   └── __init__.py  # Blueprint for authentication
- │   │   └── login.py     # Login route
- │   ├── blog/            # Blog related views
- │   │   └── __init__.py  # Blueprint for blog
- │   │   └── about.py     # About route
- │   │   └── tos.py       # Terms of Service route
- │   │   └── pp.py        # Privacy Policy route
- │   ├── static/          # Static files (CSS, JS, etc.)
- │   │   └── css/         # Stylesheets
- │   │   └── js/          # JavaScript
- │   └── templates/       # HTML templates
- │       ├── index.html   # Home page
- │       ├── auth/        # Authentication templates
- │       │   └── login.html
- │       ├── blog/        # Blog-related templates
- │       │   ├── about.html
- │       │   ├── TOS.html
- │       │   └── PP.html
- ├── config.py            # Configuration settings (e.g., app settings, database)
- ├── run.py               # To run the application
- ├── venv/                # Virtual environment
- └── requirements.txt     # List of dependencies
