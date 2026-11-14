
import json
from unittest.mock import patch, MagicMock

from ResumeIQ.ml_engine.src.extraction.resume_parser import (
    parse_resume
)


# Simulated valid model output using the actual 15-field schema.
sample_output = {
    "current_title": "Python Developer",
    "previous_titles": ["Junior Developer"],
    "current_company": "ABC Technologies",
    "previous_companies": ["XYZ Solutions"],
    "years_experience": 2.0,
    "seniority": "Junior",
    "primary_domain": "Software Development",
    "industries": ["Technology"],
    "core_skills": ["Python", "SQL"],
    "secondary_skills": ["Machine Learning"],
    "tools": ["Git", "VS Code"],
    "leadership_experience": False,
    "key_achievements": ["Developed an automation application"],
    "location": "Bengaluru",
    "summary": "Python developer with 2 years of experience."
}

generated_text = json.dumps(sample_output)

# Simulated extracted resume.
fake_resume_data = {
    "file_name": "sample_resume.pdf",
    "original_text": "Original resume content",
    "cleaned_text": "Python Developer with 2 years of experience.",
    "normalized_text": "python developer with 2 years of experience."
}

# Mock model objects.
fake_tokenizer = MagicMock()
fake_model = MagicMock()


with patch(
    "ResumeIQ.ml_engine.src.extraction.resume_parser.extract_resume",
    return_value=fake_resume_data
) as mock_extract:

    with patch(
        "ResumeIQ.ml_engine.src.extraction.resume_parser.model_manager.get_model",
        return_value=(fake_tokenizer, fake_model)
    ) as mock_model_manager:

        with patch(
            "ResumeIQ.ml_engine.src.extraction.resume_parser.generate_resume_output",
            return_value=generated_text
        ) as mock_inference:

            result = parse_resume("sample_resume.pdf")


# Verify final output.
assert result["file_name"] == "sample_resume.pdf"

assert result["resume_data"]["current_title"] == "Python Developer"

assert result["resume_data"]["core_skills"] == ["Python", "SQL"]

assert len(result["resume_data"]) == 15

# Verify that every pipeline stage was called.
mock_extract.assert_called_once_with("sample_resume.pdf")
mock_model_manager.assert_called_once()
mock_inference.assert_called_once()

print("Complete pipeline integration test passed!")
print("File:", result["file_name"])
print("Current title:", result["resume_data"]["current_title"])
print("Core skills:", result["resume_data"]["core_skills"])
print("Total extracted fields:", len(result["resume_data"]))
