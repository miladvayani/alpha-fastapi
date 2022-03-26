"""
    -- for use in services and call in checker class
"""


from fastapi import Request
from abc import ABC, abstractmethod


class IPermission(ABC):
    @abstractmethod
    def check_access(self, request: Request):
        """Function for check permission access (every driven class must impeliment)

        Args:
            request (Request): request for get user information

        Raises:
            NotImplementedError: if the driven class didn't implement the function
        """
        raise NotImplementedError

    @abstractmethod
    def _does_not_have_access(self):
        """Raises access denied error

        Raises:
            NotImplementedError: if the driven class didn't implement the function
        """
        raise NotImplementedError
