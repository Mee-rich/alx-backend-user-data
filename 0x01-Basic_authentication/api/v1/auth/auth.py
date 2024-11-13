#!/usr/bin/env python3
""" APi authentication module
"""

from flask import request
from typing import List, TypeVar

class Auth():
    """ An authentication class
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Define which routes don't need authentication
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if path == excluded_path:
                return False
                
        return True
    
    
    def authorization_header(self, request=None) -> str:
        """
            Authorization
        """
        
        if request is None:
            return None
        
        return request.headers.get('Authorization', None)
    
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
            Current User
        """
        
        return None
