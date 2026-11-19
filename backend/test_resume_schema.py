
from datetime import datetime

from app.schemas.resume import ResumeResponse


resume_data = {
    "id": 1,
    "filename": "my_resume.pdf",
    "created_at": datetime.now()
}

response = ResumeResponse(**resume_data)

print(response.model_dump())
print("Resume schema working successfully!")
