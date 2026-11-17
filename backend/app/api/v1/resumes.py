
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    HTTPException,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse

from app.services.resume_service import (
    list_user_resumes,
    save_resume_record,
    get_user_resume,
    remove_user_resume,
)


# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# Upload configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB

# Upload directory
UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Resume API router
resume_router = APIRouter()


# GET: Retrieve all resumes belonging to the logged-in user
@resume_router.get(
    "/",
    response_model=list[ResumeResponse]
)
def get_my_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = list_user_resumes(
        db=db,
        user_id=current_user.id,
    )

    return resumes


# GET: Retrieve a specific resume belonging to the logged-in user
@resume_router.get(
    "/{resume_id}",
    response_model=ResumeResponse
)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        resume = get_user_resume(
            db=db,
            resume_id=resume_id,
            user_id=current_user.id
        )

        return resume

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


# GET: Download a resume belonging to the logged-in user
@resume_router.get("/{resume_id}/download")
def download_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Step 1: Retrieve resume and verify ownership
        resume = get_user_resume(
            db=db,
            resume_id=resume_id,
            user_id=current_user.id
        )

        # Step 2: Resolve the physical file path
        file_path = Path(resume.file_path).resolve()

        # Step 3: Prevent access outside the upload directory
        if not file_path.is_relative_to(UPLOAD_DIR.resolve()):
            raise HTTPException(
                status_code=400,
                detail="Invalid resume file path"
            )

        # Step 4: Check whether the file exists
        if not file_path.is_file():
            raise HTTPException(
                status_code=404,
                detail="Resume file not found"
            )

        # Step 5: Determine the file type
        media_types = {
            ".pdf": "application/pdf",
            ".docx": (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        }

        media_type = media_types.get(file_path.suffix.lower())

        if media_type is None:
            raise HTTPException(
                status_code=400,
                detail="Unsupported resume file type"
            )

        # Step 6: Return the physical file
        return FileResponse(
            path=file_path,
            filename=resume.filename,
            media_type=media_type
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


# DELETE: Delete a resume belonging to the logged-in user
@resume_router.delete(
    "/{resume_id}",
    status_code=204
)
def delete_my_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        remove_user_resume(
            db=db,
            resume_id=resume_id,
            user_id=current_user.id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Resume record deleted, but file cleanup failed"
        )


# Validate uploaded resume
def validate_resume_file(file: UploadFile):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed",
        )

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type",
        )

    return extension


# Save uploaded resume using chunk-based reading
async def save_uploaded_file(file: UploadFile):

    file_path = None

    try:
        # Step 1: Validate uploaded file
        extension = validate_resume_file(file)

        # Step 2: Generate a unique filename
        unique_filename = f"{uuid.uuid4()}{extension}"

        file_path = UPLOAD_DIR / unique_filename

        total_size = 0

        # Step 3: Save file in chunks
        with open(file_path, "wb") as f:

            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                # Step 4: Enforce maximum file size
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Resume file cannot exceed 5 MB",
                    )

                f.write(chunk)

        return unique_filename

    except Exception:
        # Remove partially saved file if an error occurs
        if file_path is not None:
            file_path.unlink(missing_ok=True)

        raise

    finally:
        # Always close uploaded file
        await file.close()


# POST: Upload a resume for the logged-in user
@resume_router.post(
    "/",
    response_model=ResumeResponse,
    status_code=201
)
async def upload_resume(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1: Save the physical resume file
    saved_filename = await save_uploaded_file(file)

    file_path = UPLOAD_DIR / saved_filename

    try:
        # Step 2: Save resume metadata in the database
        resume = save_resume_record(
            db=db,
            user_id=current_user.id,
            filename=file.filename,
            file_path=str(file_path),
        )

        # Step 3: Return saved resume information
        return resume

    except Exception:
        # Remove physical file if database operation fails
        file_path.unlink(missing_ok=True)
        raise
