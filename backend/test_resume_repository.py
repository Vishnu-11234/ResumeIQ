
from app.database import SessionLocal
from app.repositories.resume_repository import (
    create_resume,
    get_resume_by_id,
    get_resumes_by_user,
    delete_resume
)

db = SessionLocal()

try:
    # Test using an existing user ID
    user_id = 1

    # 1. Create a resume record
    resume = create_resume(
        db=db,
        user_id=user_id,
        filename="test_resume.pdf",
        file_path="uploads/1/test_resume.pdf"
    )

    print("Created resume:", resume.id, resume.filename)

    # 2. Retrieve resume by ID and owner
    found_resume = get_resume_by_id(
        db=db,
        resume_id=resume.id,
        user_id=user_id
    )

    print("Found resume:", found_resume.filename if found_resume else None)

    # 3. Retrieve all resumes belonging to user
    user_resumes = get_resumes_by_user(
        db=db,
        user_id=user_id
    )

    print("User resumes:", [r.filename for r in user_resumes])

    # 4. Test ownership protection
    wrong_owner = get_resume_by_id(
        db=db,
        resume_id=resume.id,
        user_id=999
    )

    print("Wrong owner result:", wrong_owner)

    # 5. Delete resume record
    deleted = delete_resume(
        db=db,
        resume_id=resume.id,
        user_id=user_id
    )

    print("Deleted:", deleted)

finally:
    db.close()
