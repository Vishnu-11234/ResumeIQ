
from ResumeIQ.ml_engine.src.preprocessing.text_normalizer import (
    normalize_resume_text
)

sample_text = """
PYTHON Developer

Machine   Learning
REST APIs
"""

normalized_text = normalize_resume_text(sample_text)

print("Normalized text:")
print(normalized_text)

assert "python developer" in normalized_text
assert "machine learning" in normalized_text
assert "rest apis" in normalized_text

print("\nAll tests passed!")
