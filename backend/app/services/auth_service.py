
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)




def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    """
    Handle the business logic for user registration.
    """

    # 1. Check whether the email already exists
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("Email already registered")

    # 2. Hash the original password
    hashed_password = hash_password(password)

    # 3. Save the user through the repository
    new_user = create_user(
        db=db,
        name=name,
        email=email,
        hashed_password=hashed_password
    )

    return new_user

def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    """
    Authenticate a user using email and password.
    """

    # 1. Find user using email
    user = get_user_by_email(db, email)

    # 2. Check whether user exists
    if not user:
        raise ValueError("Invalid email or password")

    # 3. Verify entered password against stored hash
    is_password_valid = verify_password(
        password,
        user.hashed_password
    )

    if not is_password_valid:
        raise ValueError("Invalid email or password")

    # 4. Return authenticated user
    return user
