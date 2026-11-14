
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    UserRegister,
    UserResponse,
    UserLogin,
    TokenResponse
)
from app.services.auth_service import (
    register_user,
    authenticate_user
)
from app.core.security import (
    get_current_user,
    create_access_token
)
from app.models.user import User


auth_router = APIRouter()


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    try:
        new_user = register_user(
            db=db,
            name=user_data.name,
            email=str(user_data.email),
            password=user_data.password
        )

        return new_user

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
@auth_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Return the profile of the currently authenticated user.
    """
    return current_user
@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(
            db=db,
            email=str(user_data.email),
            password=user_data.password
        )

        access_token = create_access_token(user.id)

        return TokenResponse(
            access_token=access_token
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )