# Projekt-OSPR
Projekt za OSPR
#TODO
```md
- []Cpanel - py flask, html
    - [x]console
    - [x]settings
    - [x]cpanel
    - []user settings
- [x]Home Page - html
- [x]Blog - html
    - [x]about - html
    - [x]TOS - html
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

  Addon:
  - [x]TailWind
  - [x]Bootstrap
  - [x]1 File for primary settings - css
  - []SQL - Database - Data stealing
  - []Mini games - loading screens

```


Resources:
- https://firebase.google.com/ - database
- https://github.com/Jonontop/Projekt-OSPR
- https://flask.palletsprojects.com/en/stable/api/ - flask
- https://flask.palletsprojects.com/en/stable/tutorial/templates/ - flask templates
- https://medium.com/@andrii.gorshunov/paypal-flask-integration-python-2022-1c012322801d - paypal integration
- https://www.docker.com/ - docker API
- 


# Structure:
```md
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
- │       ├── payment/      # Payment-related templates - not implemented yet
- │       │   ├── payment.html
- │       │   └── plans.html
- ├── config.py            # Configuration settings (e.g., app settings, database)
- ├── run.py               # To run the application
- ├── venv/                # Virtual environment
- └── requirements.txt     # List of dependencies

```

Postopek za zagon:
```bash
# 1. Clone the repository
git clone
# 2. Navigate to the project directory
cd Projekt-OSPR
# 3. Create a virtual environment
python -m venv venv
# 4. Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# 5. Install the required packages
pip install -r requirements.txt
# 6. Set up connection to Docker
# Make sure Docker is running on your local machine - remote connection can be set in docker.py:19
# 7. Run the application
python run.py
```


## Function Descriptions

### DockerManager Class

This class handles Docker container operations for server management.

| Function         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `docker_create`  | Creates a new Docker container with specified server parameters (name, CPU, storage, RAM) using a predefined template. |
| `docker_stop`    | Stops a running Docker container identified by container ID.               |
| `docker_start`   | Starts a stopped Docker container identified by container ID.              |
| `docker_delete`  | Stops and removes a Docker container, performing complete cleanup.         |
| `docker_restart` | Restarts a running Docker container.                                       |
| `stream_logs`    | Streams real-time logs from a container as server-sent events.            |
| `container_stats`| Retrieves and calculates resource usage statistics (CPU, memory, disk) for a container. |

### DockerFiles Class

This class handles file operations within Docker containers.

| Function               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `build_tree`           | Constructs a hierarchical file structure representation from a flat file list. |
| `docker_download_file` | Downloads a file from a container to the host system.                      |
| `docker_delete_file`   | Deletes a file inside a container.                                         |
| `docker_edit_file`     | Modifies the contents of an existing file in a container.                  |
| `docker_create_file`   | Creates a new file with specified content in a container.                  |
| `docker_upload_file`   | Uploads a file from the host system to a container.                        |
| `docker_display_files` | Lists all files in container volumes and builds a file tree representation. |
| `docker_create_folder` | Creates a new directory inside a container.                               |

### Database Class

This class manages database operations for server management.

| Function         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `server_create`  | Creates a new server record in the database with specified configuration parameters. |
| `server_delete`  | Removes a server record from the database by container ID.                 |
| `get_server_stats`| Retrieves comprehensive server statistics and configuration from the database. |
| `server_update`  | Updates server configuration parameters in the database.                  |

### Auth Class

This class handles user authentication with Firebase.

| Function       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `register`     | Registers a new user with Firebase Authentication and creates a user record in Firestore. |
| `logout`       | Logs out the current user by clearing session data and cookies.            |
| `TokenVerify`  | Verifies a Firebase ID token and establishes a user session.               |

### Model Functions

| Function             | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `load_server_templates` | Loads server template configurations from a JSON file.                  |
| `auth_required`      | Decorator that requires user authentication for protected routes.          |
| `TokenVerify`        | Verifies a Firebase ID token and establishes a user session.              |
| `Webhook`            | Sends a message to a Discord webhook with specified content and username. |
