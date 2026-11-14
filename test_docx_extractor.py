
from ResumeIQ.ml_engine.src.extraction.docx_extractor import (
    extract_text_from_docx
)

docx_path = r"D:\path\to\your\resume.docx"

try:
    text = extract_text_from_docx(docx_path)

    print("DOCX extraction successful!")
    print("Extracted characters:", len(text))
    print("\nExtracted text:\n")
    print(text)

except Exception as error:
    print("Extraction failed:", error)
