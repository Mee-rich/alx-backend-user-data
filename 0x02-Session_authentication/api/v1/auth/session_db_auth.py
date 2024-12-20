#!/usr/bin/env pyhton3
""" Session authentication Database system
"""

from flask import request
from datetime import datetime, timedelta

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """Session authentication Database to store 
        session ids
    """

    def create_session(self, user_id=None) -> str:
        """Creates a sessionDBAuth instance
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                    'user_id': user_id,
                    'session_id': session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets the user id of user session in the 
            database based on session_id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        curr_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < curr_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys the user session based on the 
            session id from the request cookie
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        session[0].remove()
        return True


