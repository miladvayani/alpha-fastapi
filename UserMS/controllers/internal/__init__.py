from UserMS import Application as root
from fastapi import APIRouter


rabbit = root.rabbit_manager.router
api = APIRouter(prefix="/v2/internal", tags=["Internal"])

from .views.user import *
