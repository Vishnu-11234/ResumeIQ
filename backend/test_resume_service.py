
from app.database import SessionLocal

from app.services.resume_service import (
    save_resume_record,
    get_user_resume,
    list_user_resumes,
    remove_user_resume
)

db = SessionLocal()

try:
    user_id = 1

    # TEST 1: Create a resume
    resume = save_resume_record(
        db=db,
        user_id=user_id,
        filename="service_test.pdf",
        file_path="uploads/1/service_test.pdf"
    )

    print("Created:", resume.id, resume.filename)

    # TEST 2: Retrieve the resume
    found = get_user_resume(
        db=db,
        resume_id=resume.id,
        user_id=user_id
    )

    print("Retrieved:", found.filename)

    # TEST 3: Retrieve all user resumes
    resumes = list_user_resumes(
        db=db,
        user_id=user_id
    )

    print("User resumes:", [r.filename for r in resumes])

    # TEST 4: Test wrong ownership
    try:
        get_user_resume(
            db=db,
            resume_id=resume.id,
            user_id=999
        )
    except ValueError as error:
        print("Ownership protection:", error)

    # TEST 5: Delete the resume
    deleted = remove_user_resume(
        db=db,
        resume_id=resume.id,
        user_id=user_id
    )

    print("Deleted:", deleted)

finally:
    db.close()
