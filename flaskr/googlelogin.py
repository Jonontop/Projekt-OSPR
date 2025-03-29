from flask import Blueprint, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
import os

# Ustvari Google blueprint s pravilnimi vrednostmi iz okolja
google_bp = make_google_blueprint(
    client_id=os.environ.get("895371472700-so2hqv67c4fvipff2f8r4strcrmmg1ao.apps.googleusercontent.com"),
    client_secret=os.environ.get("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"),
    redirect_to="google_login",  # Preusmeritev na funkcijo po prijavi
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]
)


# Dodatna pot za preverjanje uspešne prijave
@google_bp.route("/google/callback")
def google_login():
    if not google.authorized:
        print("Google NI pooblaščen!")
        flash("Google Sign-In failed!", "error")
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        print(f"Napaka pri pridobivanju uporabniških podatkov: {resp.text}")
        flash("Napaka pri prijavi", "error")
        return redirect(url_for("index"))

    user_info = resp.json()
    print(f"Prijavljen uporabnik: {user_info}")
    session['user'] = user_info
    flash("Uspešna prijava!", "success")
    return redirect(url_for('index'))
