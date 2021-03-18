# Standard Imports
from os import name
from fastapi import Depends
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
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


manager = LoginManager(JWT_SECRET, tokenUrl=API_PREFIX+'/auth/token')
route = APIRouter()


# Login Schema
class LoginData(BaseSchema):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "dudu@mail.com",
                "password": "mysecretpassword"
            }
        }

@manager.user_loader
def load_user(username: str):
    db = next(get_db())
    user = db.query(User).filter(or_(
        User.email == username,
        User.email == username
    )).first()
    return user

@route.post('/auth/token', include_in_schema=False)
def auth_token(data: OAuth2PasswordRequestForm = Depends()):
    return login(data)

@route.post('/login')
def login(data: LoginData):
    username = data.username
    password = data.password

    user: User = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif user.verify_password(password) == False:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username),
        expires=timedelta(days=JWT_EXPIRATION_DAYS)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}



# Route for test authentication
from ..modules.users.schemas import UserResponse
from ..modules.providers.models import Provider
from ..modules.products.models import Product, ProductImage
from ..modules.transactions.models import Transaction
from sqlalchemy.orm import Session

@route.get('/auth/protected', response_model=UserResponse)
def test_authentication(user: User=Depends(manager), db: Session = Depends(get_db)):

    # provider = Provider(name="Teste Fornecedor", cnpj="00000000000000", created_by=user.id)
    # provider = provider.insert(db)
    
    # product = Product(name="Teste Produto", size="10", inventory=1, created_by=user.id)
    # image = ProductImage()
    # product.image.append(image)
    # product.providers.append(provider)
    # product = product.insert(db)


    # provider: Provider = db.query(Provider).get(1)
    # product: Product = db.query(Product).get(1)
    # product.providers.append(provider)
    # image = ProductImage()
    # product.image.append(image)
    # product = product.insert(db)





    return user