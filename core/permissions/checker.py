"""
    -- for use in endpoints and interact with permission interfaces with no service interference 
"""


from fastapi import Request
from .interface import IPermission


class PermissionChecker:
    def __init__(self, p: IPermission):
        self.__permission = p

    def check(self, request: Request):
        """Function for call defined service check_access function

        Args:
            request (Request): request
        """
        self.__permission.check_access(request)
