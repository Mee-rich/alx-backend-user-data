#!/usr/bin/env python3
""" This is an authentication module
"""

from flask import request
from typing import List, TypeVar
import fnmatch

class Auth:
    """ A basic authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authentication
        """
        if not path or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True


    def authorization_header(self, request=None) -> str:
        """ Gets the authorization field from the request header
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets the current user from the request
        """
        
        return None
