from typing import Literal

from pydantic import BaseModel, Field


class ResumeAnalysisRequest(BaseModel):
    resume_text: str = Field(
        min_length=1,
        description="Extracted text from the resume"
    )


class ResumeAnalysisResponse(BaseModel):
    current_title: str | None
    previous_titles: list[str]

    current_company: str | None
    previous_companies: list[str]

    years_experience: float | None
    seniority: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
        "executive",
        "unknown"
    ]

    primary_domain: str | None
    industries: list[str]

    core_skills: list[str]
    secondary_skills: list[str]
    tools: list[str]

    leadership_experience: bool
    key_achievements: list[str]

    location: str | None
    summary: str | None