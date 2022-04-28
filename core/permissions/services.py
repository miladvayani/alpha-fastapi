"""
for various permissions and inherit from IPermission to use its functions
 
    -- if you want to add new permission role:
        add your class there and implement IPermission functions like others
"""

from bson import ObjectId
from fastapi import Request, HTTPException
from .interface import IPermission


class WorkspaceUser(IPermission):
    def check_access(self, request: Request):
        if not bool(request.state.user and request.state.user.is_authenticated):
            return self._does_not_have_access()

    def _does_not_have_access(self):
        raise HTTPException(status_code=401)


class WorkspaceOwner(IPermission):
    def check_access(self, request: Request):
        request.state.user.workspace = ObjectId(request.state.user.workspace)
        if not bool(
            request.state.user
            and request.state.user.is_authenticated
            and request.state.user.is_owner
        ):
            return self._does_not_have_access()

    def _does_not_have_access(self):
        raise HTTPException(status_code=401)


class UserAuthenticated(IPermission):
    def check_access(self, request: Request):
        if not bool(request.state.user and request.state.user.is_authenticated):
            return self._does_not_have_access()

    def _does_not_have_access(self):
        raise HTTPException(status_code=401)
