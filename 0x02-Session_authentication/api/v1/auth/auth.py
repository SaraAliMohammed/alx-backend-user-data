#!/usr/bin/env python3
"""
A module for the Auth class
"""
from flask import request
from tabnanny import check
from typing import TypeVar, List
from os import getenv
User = TypeVar('User')


class Auth:
    """
    A class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path and excluded_paths
        """
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        returns None - request
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        returns None - request
        """
        return None

    def session_cookie(self, request=None):
        """ Returns cookie value from a request """
        if request is None:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))
