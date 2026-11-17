
from pathlib import Path

from sqlalchemy.orm import Session

from app.repositories.resume_repository import (
    create_resume,
    get_resume_by_id,
    get_resumes_by_user,
    delete_resume
)


UPLOAD_DIR = Path("uploads/resumes").resolve()


def save_resume_record(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str
):
    """
    Save resume metadata for an authenticated user.
    """

    return create_resume(
        db=db,
        user_id=user_id,
        filename=filename,
        file_path=file_path
    )


def get_user_resume(
    db: Session,
    resume_id: int,
    user_id: int
):
    """
    Retrieve a specific resume belonging to a user.
    """

    resume = get_resume_by_id(
        db=db,
        resume_id=resume_id,
        user_id=user_id
    )

    if resume is None:
        raise ValueError("Resume not found")

    return resume


def list_user_resumes(
    db: Session,
    user_id: int
):
    """
    Retrieve all resumes belonging to a user.
    """

    return get_resumes_by_user(
        db=db,
        user_id=user_id
    )


def remove_user_resume(
    db: Session,
    resume_id: int,
    user_id: int
):
    """
    Delete a resume record and its physical file.
    """

    # 1. Find the resume and verify ownership.
    resume = get_resume_by_id(
        db=db,
        resume_id=resume_id,
        user_id=user_id
    )

    if resume is None:
        raise ValueError("Resume not found")

    # 2. Resolve the physical file path.
    file_path = Path(resume.file_path).resolve()

    # 3. Ensure the file is inside the resume upload directory.
    if not file_path.is_relative_to(UPLOAD_DIR):
        raise RuntimeError("Invalid resume file path")

    # 4. Delete the database record.
    deleted = delete_resume(
        db=db,
        resume_id=resume_id,
        user_id=user_id
    )

    if not deleted:
        raise ValueError("Resume not found")

    # 5. Delete the physical file.
    try:
        file_path.unlink(missing_ok=True)

    except OSError as error:
        raise RuntimeError(
            "Resume record deleted, but physical file cleanup failed"
        ) from error

    return True
