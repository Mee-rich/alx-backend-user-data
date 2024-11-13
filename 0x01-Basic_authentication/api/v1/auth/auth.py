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
        if path and not path.endswith('/'):
            path = path + ('/')
        if not path or path not in excluded_paths:
            return True
        if  not excluded_paths or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
                
        return True
    
    
    def authorization_header(self, request=None) -> str:
        """
            Authorization
        """
        
        if request is None:
            return None
        
        header = request.headers.get('Authorization')
        
        if header is None:
            return None
        
        return header
    
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
            Current User
        """
        
        return None
