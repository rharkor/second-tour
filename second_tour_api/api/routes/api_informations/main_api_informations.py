from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()

from database.config import db

@router.get('/')
def get_version_of_the_api():
    check = JSONResponse(status_code=status.HTTP_200_OK, content={'version': "1.0.0"})
    return check