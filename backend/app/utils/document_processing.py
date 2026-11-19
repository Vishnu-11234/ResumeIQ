
from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF resume."""

    reader = PdfReader(file_path)

    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()


def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    extracted_text = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            extracted_text.append(text)

    # Extract table contents
    for table in document.tables:
        for row in table.rows:
            row_text = " | ".join(
                cell.text.strip() for cell in row.cells
                if cell.text.strip()
            )

            if row_text:
                extracted_text.append(row_text)

    return "\n".join(extracted_text).strip()


def extract_resume_text(file_path: str | Path) -> str:
    """Extract text from PDF or DOCX resume."""

    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif extension == ".docx":
        text = extract_text_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Only PDF and DOCX are supported."
        )

    if not text.strip():
        raise ValueError(
            "No readable text found in resume. "
            "The file may be scanned or empty."
        )

    return text
