#!/usr/bin/env python3
""" A Base64 authentication module
"""

from .auth import Auth
import re
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User

class BasicAuth(Auth):
    """ An implementation of a Base64 authentication
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the authorization header
            of a Basic Authentication
        """
        if not isinstance(authorization_header, str):
            return None

        # Use regex to match "Basic <Base64-token>"
        pattern = r'^Basic (?P<token>.+)$'
        match = re.fullmatch(pattern, authorization_header.strip())
        if match:
            return match.group('token')
        return None


    def decode_extract_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string
        """
        if isinstance(base64_authorization_header, str):
            try:
                res = base64.b64decode(
                        base64_authorization_header,
                        validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Returns the user email and password from the
            Base64 decoded value
        """

        if isinstance (decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(pattern, decoded_base64_authorization_header
            )

            if match is not None:
                user = match.group('user')
                password = match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the user instance based on his email and password
        """
        if all(isinstance(x, str) for x in [user_email, user_pwd]):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the user instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_extract_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
