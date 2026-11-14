
from ResumeIQ.ml_engine.src.extraction.resume_extractor import (
    extract_resume
)

resume_path = r"D:\data\data\ENGINEERING\10219099.pdf"

try:
    result = extract_resume(resume_path)

    print("Resume extraction successful!")

    print("\nFile:", result["file_name"])

    print("\nOriginal text length:",
          len(result["original_text"]))

    print("Cleaned text length:",
          len(result["cleaned_text"]))

    print("Normalized text length:",
          len(result["normalized_text"]))

    print("\nCleaned resume:")
    print(result["cleaned_text"][:1500])

except Exception as error:
    print("Pipeline failed:", error)

