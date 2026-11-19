from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.services.resume_service import get_user_resume
from app.utils.document_processing import extract_resume_text
from app.services.analysis_service import (
    analyze_resume_text,
    AIEngineConnectionError,
    AIEngineResponseError,
)


analysis_router = APIRouter()


@analysis_router.post("/{resume_id}")
async def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Step 1: Retrieve resume and verify ownership
    try:
        resume = get_user_resume(
            db=db,
            resume_id=resume_id,
            user_id=current_user.id,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    # Step 2: Get the physical file path
    file_path = Path(resume.file_path)

    # Step 3: Check whether the file exists
    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found",
        )

    # Step 4: Extract text from the resume
    try:
        resume_text = extract_resume_text(file_path)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    # Step 5: Send extracted text to the AI Engine
    try:
        analysis = await analyze_resume_text(resume_text)

    except AIEngineConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except AIEngineResponseError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )

    # Step 6: Return analysis to the client
    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "analysis": analysis,
    }