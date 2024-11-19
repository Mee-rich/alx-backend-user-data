#!/usr/bin/env pyhton3
"""Suthentication system that stores session id
    in database
"""

from .base import Base


class UserSession(Base):
    """User session authentication system
    """

    def __init__(self, *args: list, **Kwargs: dict):
        """Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
