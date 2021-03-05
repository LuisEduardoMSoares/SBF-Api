# Standard Imports
from fastapi import Depends
from fastapi import APIRouter
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy import or_
from datetime import timedelta

from .. import API_PREFIX
from ..utils.helpers import BaseSchema

# Environment Import
from .config import JWT_SECRET
from .config import JWT_EXPIRATION_DAYS

# Database Import
from ..db.engine import get_db
from ..modules.users.models import User


manager = LoginManager(JWT_SECRET, tokenUrl=API_PREFIX+'/login')
route = APIRouter()


# Login Schema
class LoginData(BaseSchema):
    login: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "login": "dudu@mail.com",
                "password": "mysecretpassword"
            }
        }

@manager.user_loader
def load_user(login: str):
    db = next(get_db())
    user = db.query(User).filter(or_(
        User.email == login,
        User.username == login
    )).first()
    return user

@route.post('/login')
def login(data: LoginData):
    login = data.login
    password = data.password

    user: User = load_user(login)
    if not user:
        raise InvalidCredentialsException
    elif user.verify_password(password) == False:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=login),
        expires=timedelta(days=JWT_EXPIRATION_DAYS)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}



# Route for test authentication
from ..modules.users.schemas import UserResponse

@route.get('/auth/protected', response_model=UserResponse)
def test_authentication(user=Depends(manager)):
    return user
