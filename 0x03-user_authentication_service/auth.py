#!/usr/bin/env python3
"""Password hashing module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Optional, Union

from db import DB
from user import User

def _hash_password(password: str) -> bytes:
    """Hashes a password and adds a salt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generates a uuid
    """
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()


    def register_user(self, email: str, password: str) -> User:
        """Registers a user with a hashed password
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")


    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user login details are valid
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Generates a sesson id for a user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[Union[User, None]]:
        """Gets the user associated with a session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session
        """
        if user_id:
            try:
                user = self._db.find_user_by(user_id=user_id)
                self._db.update_user(user.id, session_id=None)
            except NoRecordFound:
                return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")


    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                    user.id, 
                    hashed_password=_hash_password(password), 
                    reset_token=None)
        except NoResultFound:
            raise ValueError(f"User password not updated.")


