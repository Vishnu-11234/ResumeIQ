
from pathlib import Path

from .pdf_extractor import extract_text_from_pdf
from .docx_extractor import extract_text_from_docx

from ..preprocessing.resume_cleaner import clean_resume_text
from ..preprocessing.text_normalizer import normalize_resume_text


def extract_resume(resume_path: str) -> dict:
    """
    Extract and preprocess resume content.

    Returns:
        dict containing original, cleaned and normalized text.
    """

    path = Path(resume_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {resume_path}"
        )

    extension = path.suffix.lower()

    # Select the appropriate extraction function
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(str(path))

    elif extension == ".docx":
        extracted_text = extract_text_from_docx(str(path))

    else:
        raise ValueError(
            f"Unsupported resume format: {extension}"
        )

    # Clean extracted text
    cleaned_text = clean_resume_text(extracted_text)

    # Generate normalized text
    normalized_text = normalize_resume_text(cleaned_text)

    return {
        "file_name": path.name,
        "original_text": extracted_text,
        "cleaned_text": cleaned_text,
        "normalized_text": normalized_text
    }
