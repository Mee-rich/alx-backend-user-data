#!/usr/bin/env python3
""" This module adds an expiration date to a Session ID
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    """ Adds expiration to a session-id
    """

    def __init__(self):
        """Initializing a new SessionAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0


    def create_session(self, user_id=None):
        """ Creates a new session id for the user
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                    'user_id' : user_id,
                    'created_at' : datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Gets the user id from the session id
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
