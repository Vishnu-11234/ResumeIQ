
from fastapi import FastAPI

from src.api.schemas import ResumeAnalysisRequest, ResumeAnalysisResponse
from src.llm.pipeline import analyze_resume


app = FastAPI(
    title="ResumeIQ AI Engine",
    description="AI service for resume intelligence and analysis",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ResumeIQ AI Engine"
    }


@app.post("/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume_endpoint(request: ResumeAnalysisRequest):

    result = analyze_resume(request.resume_text)

    return result
