
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import get_user_by_id
# Create one password hasher instance
password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into an Argon2id hash.
    """
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check whether the entered password matches the stored hash.
    """
    try:
        return password_hasher.verify(
            hashed_password,
            plain_password
        )

    except (VerifyMismatchError, VerificationError):
        return False



load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int) -> str:
    """
    Generate a signed JWT access token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return access_token

def verify_access_token(token: str) -> dict | None:
    """
    Verify JWT signature and expiration.
    Return the payload if valid, otherwise None.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Ensure the token identifies a user
        if not payload.get("sub"):
            return None

        return payload

    except JWTError:
        return None
# Extract Bearer token from the Authorization header
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Verify JWT and retrieve the authenticated user.
    """

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user