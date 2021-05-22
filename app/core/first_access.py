# Standard imports
from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException

# Database import
from ..db.engine import get_db

# Typing imports
from sqlalchemy.orm import Session

# Exception imports
from sqlalchemy.exc import IntegrityError

# User schemas import
from ..modules.users.schemas import UserCreate
from ..modules.users.schemas import UserResponse

# User service import
from app.modules.users.services import UserService


route = APIRouter()
user_service = UserService()


@route.post('/first-access', response_model=UserResponse)
def create_first_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    ## Create the first active admin user.

    ### Args:  
      >  user (UserCreate): The user creation model.

    ### Raises:  
      >  HTTPException: Raises 401 if already exists other admin user active.  
      >  HTTPException: Raises 422 if the email is already in use.  

    ### Returns:  
      >  UserResponse: The admin user response model.
    """
    users = user_service.fetch_all(db, only_admin=True)
    if len(users) != 0:
        raise HTTPException(status_code=401, detail="Only allowed if there is no active admin users.")

    try:
        user.admin = True
        user = user_service.create(db, user)
        return user
    except IntegrityError as err:
        if "email" in repr(err):
            raise HTTPException(status_code=422, detail="Já existe um usuário com este email cadastrado.")
