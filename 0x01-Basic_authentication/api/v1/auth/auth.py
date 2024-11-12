#!/usr/bin/env python3
""" APi authentication module
"""

from flask import request
from typing import List, TypeVar

class Auth():
    """ An authentication class
    """
    
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """
        
        """
        
        return False
    
    
    def authorization_header(self, request=None) -> str:
        """
        
        """
        
        return None
    
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        
        """
        
        return None