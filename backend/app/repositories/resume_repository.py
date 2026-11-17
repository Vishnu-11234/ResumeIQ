
from sqlalchemy.orm import Session

from app.models.resume import Resume


def create_resume(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str
):
    """
    Create and save a resume record in the database.
    """

    new_resume = Resume(
        user_id=user_id,
        filename=filename,
        file_path=file_path
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume


def get_resume_by_id(
    db: Session,
    resume_id: int,
    user_id: int
):
    """
    Retrieve a resume belonging to a specific user.
    """

    return (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        )
        .first()
    )


def get_resumes_by_user(
    db: Session,
    user_id: int
):
    """
    Retrieve all resumes belonging to a specific user.
    """

    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .all()
    )


def delete_resume(
    db: Session,
    resume_id: int,
    user_id: int
):
    """
    Delete a resume record belonging to a specific user.
    """

    resume = get_resume_by_id(
        db=db,
        resume_id=resume_id,
        user_id=user_id
    )

    if resume is None:
        return False

    try:
        db.delete(resume)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise
