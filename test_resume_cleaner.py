
from ResumeIQ.ml_engine.src.preprocessing.resume_cleaner import (
    clean_resume_text
)

raw_text = """
Python     Developer


Experience inÂ Machine Learning & AI

    Skills: Python       SQL
"""

cleaned_text = clean_resume_text(raw_text)

print("Original text:")
print(raw_text)

print("\nCleaned text:")
print(cleaned_text)

assert "Python Developer" in cleaned_text
assert "\n\n\n" not in cleaned_text

print("\nAll tests passed!")
