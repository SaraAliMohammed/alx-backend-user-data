#!/usr/bin/env python3
"""
Basic Auth module
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """
    class BasicAuth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
         returns the Base64 part of the Authorization
         header for a Basic Authentication
        """
        if authorization_header and isinstance(
                authorization_header,
                str) and authorization_header.startswith("Basic "):
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns decoded value of base64_authorization_header"""
        b64_auth_header = base64_authorization_header
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encode = b64_auth_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        decoded_64 = decoded_base64_authorization_header
        if (decoded_64 and isinstance(decoded_64, str) and
                ":" in decoded_64):
            res = decoded_64.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns User instance based on email and pswd """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)

        # Decode auth header value, get user data using Basic Auth methods
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(*user_creds)
