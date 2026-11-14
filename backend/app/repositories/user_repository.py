
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    """
    Find a user using their email address.
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    name: str,
    email: str,
    hashed_password: str
):
    """
    Save a new user in the database.
    """

    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )