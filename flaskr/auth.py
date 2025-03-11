import time

from flask import flas
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import get_firestore_client

db = get_firestore_client()

# Register user
def register_user(username:str, email:str, password:str, name:str):
    users_ref = db.collection("users")
    # Check if email already exists
    query = users_ref.where("email", "==", email).limit(1).get()
    if len(query) > 0:
        return False, "Email already exists."

    # Hash the password
    password_hash = generate_password_hash(password) # Kriptira geslo

    # Add user to Firestore
    user_data = {
        "name": name,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "firstlog": time.time(),
        "lastlog": time.time()
    }
    users_ref.add(user_data)
    return True, "User registered successfully."

# Login user
def login_user(email, password):
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email).limit(1).get()

    ## Update last login
    user_data = {
        "lastlog": time.time() # Update last login
    }

    users_ref.document(query[0].id).update(user_data) # Update last login

    if len(query) == 0:
        return False, "User not found."

    user = query[0].to_dict()
    if check_password_hash(user["password_hash"], password):
        return True, user
    else:
        return False, "Invalid password."


