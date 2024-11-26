import requests

BASE_URL = "http://localhost:5000"  # Replace with your actual base URL

def register_user(email: str, password: str) -> None:
    """Registers a user."""
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    """Tries to log in with a wrong password."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401
    assert res.json() == {"message": "invalid credentials"}

def log_in(email: str, password: str) -> str:
    """Logs in a user and returns the session ID."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    response_json = res.json()
    assert "session_id" in response_json
    return response_json["session_id"]

def profile_unlogged() -> None:
    """Tries to access the profile without being logged in."""
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403
    assert res.json() == {"message": "unauthorized"}

def profile_logged(session_id: str) -> None:
    """Accesses the profile while logged in."""
    url = "{}/profile".format(BASE_URL)
    cookies = {'session_id': session_id}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    assert "email" in res.json()

def log_out(session_id: str) -> None:
    """Logs out a user."""
    url = "{}/sessions".format(BASE_URL)
    cookies = {'session_id': session_id}
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "session destroyed"}

def reset_password_token(email: str) -> str:
    """Generates a password reset token."""
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    response_json = res.json()
    assert "reset_token" in response_json
    return response_json["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the password of a user."""
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    # Register user
    register_user(EMAIL, PASSWD)
    
    # Log in with wrong password
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    
    # Try to access profile without being logged in
    profile_unlogged()
    
    # Log in with correct password and get session_id
    session_id = log_in(EMAIL, PASSWD)
    
    # Access profile while logged in
    profile_logged(session_id)
    
    # Log out
    log_out(session_id)
    
    # Generate reset password token
    reset_token = reset_password_token(EMAIL)
    
    # Update password with the reset token
    update_password(EMAIL, reset_token, NEW_PASSWD)
    
    # Log in with new password
    log_in(EMAIL, NEW_PASSWD)

