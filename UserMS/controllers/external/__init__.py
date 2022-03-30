from fastapi import APIRouter, Depends
from ...core.permissions.services import UserAuthenticated
from ...core.permissions.checker import PermissionChecker

router = APIRouter(
    prefix="/v2",
    tags=["External"],
    dependencies=[Depends(PermissionChecker(UserAuthenticated()).check)],
)

from .views.user import *
from .views.legal import *
