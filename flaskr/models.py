from flask_login import UserMixin
from flaskr import get_firestore_client

db = get_firestore_client()

class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    # Static method to get a user from Firestore
    @staticmethod
    def get(user_id):
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        if user.exists:
            user_data = user.to_dict()
            return User(user_id, user_data["username"], user_data["email"])
        return None