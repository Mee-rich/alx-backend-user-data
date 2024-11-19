#!/usr/bin/env python3
""" A module for session authentication
"""

from .auth import Auth
from uuid import uuid4
from models.user import User

class SessionAuth(Auth):
    """ Session authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id
        """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets a user ID based on session ID
        """
        if isinstance(session_id, str):
            user_id = self.user_id_by_session_id.get(session_id)
            return user_id

    def current_user(self, request=None):
        """ Gets a user instance based on a cookie value
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session/logout
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if not any([request, session_id, user_id]):
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True

