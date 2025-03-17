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
- [x]Home Page - html
- []Blog - html
    - []about - html
    - [x]TOS - html
    - []PP - html
- []Error - html
    - [x]404 - html
    - [x]500 - html
- [x]Login - flask login
    - Login/Register Website - FireBase, html, py
- []Payment System - flask paypal
- [x]DataBase - firebase
    - [x]connection
    - [x]user's info
    - [x]user's general info
    - [x]Google Analitics
- [x]Plans site - html
- []currency acquering system - firebase, py

  Addon:
  - []TailWind
  - []Bootstrap
  - []DarkMode
  - [x]1 File for primary settings - css
  - []SQL - Data stealing
  - []Minigames - loading screens, coins collecting




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
