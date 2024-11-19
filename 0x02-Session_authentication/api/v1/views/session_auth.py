#!/usr/bin/env python3
""" Module for session authentication views
"""
from os import getenv
from flask import abort, jsonify, request
from typing import Tuple
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
        - JSON representation of a user object
    """
    not_found_res = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404
    if len(users) <= 0:
        return jsonify(not_found_res), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        cookie_name = getenv("SESSION_NAME", "_my_session_id")
        res.set_cookie(cookie_name, session_id)
        return res
    return jsonify({"error": "wrong password"})

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
        - An empty JSON object
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
