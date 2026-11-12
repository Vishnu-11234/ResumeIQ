from ResumeIQ.ml_engine.src.extraction.pdf_extractor import (
    extract_text_from_pdf
)

pdf_path = r"D:\data\data\ENGINEERING\10219099.pdf"
try:
    text = extract_text_from_pdf(pdf_path)

    print("PDF extraction successful!")
    print("Extracted characters:", len(text))
    print("\nExtracted text:\n")
    print(text)

except Exception as error:
    print("Extraction failed:", error)
