#!/usr/bin/env python3
"""A basic Flask app
"""

from flask import Flask, jsonify, request, abort, redirect
from user import User
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
        {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Return:
        {"email": "<registered email>", "message": "user created"}
        otherwise {"message": "email already registered"}
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - {"email": "<user email>", "message": "logged in"}
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - 403 HTTP status if user does not exist
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect ("/")
    else:
        abort(403)

@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - {"email": "<user email>"} 200 HTTP status
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)

@app.route("/reset_password", methods=["GET"], strict_slashes=False)
def get_reset_password() -> str:
    """Reset the password of a user
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        reset_token = None
        abort(403, f"Invalid email or reset token request failed.")
    

@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Update the password for a user
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(
                reset_token, 
                new_password
            )
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError as e:
        abort(403, f"An error occured while updating {email}'s password: {e}")
    except Exception as e:
        abort(500, f"An unexpected error occurred while updating {email}'s password: {e}")






if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
