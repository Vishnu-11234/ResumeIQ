
from ResumeIQ.ml_engine.src.preprocessing.resume_cleaner import (
    clean_resume_text
)

from ResumeIQ.ml_engine.src.preprocessing.text_normalizer import (
    normalize_resume_text
)


def preprocess_resume_text(text: str) -> str:

    cleaned_text = clean_resume_text(text)

    normalized_text = normalize_resume_text(cleaned_text)

    return normalized_text


sample_text = """
PYTHON     Developer


Experience in Machine   Learning

Skills: Python       SQL
"""

result = preprocess_resume_text(sample_text)

print("Preprocessed resume:")
print(result)
assert "python developer" in result
assert "machine learning" in result
assert "skills: python sql" in result

print("\nPreprocessing pipeline passed!")
