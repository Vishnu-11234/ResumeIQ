
from pathlib import Path
from docx import Document


def extract_text_from_docx(docx_path: str) -> str:

    path = Path(docx_path)

    if not path.exists():
        raise FileNotFoundError(f"DOCX file not found: {docx_path}")

    if path.suffix.lower() != ".docx":
        raise ValueError("Provided file is not a DOCX")

    try:
        document = Document(str(path))

        extracted_content = []

        # Extract paragraphs
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                extracted_content.append(text)

        # Extract tables
        for table in document.tables:
            for row in table.rows:
                row_text = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]

                if row_text:
                    extracted_content.append(" | ".join(row_text))

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract DOCX text: {error}"
        ) from error

    full_text = "\n\n".join(extracted_content).strip()

    if not full_text:
        raise ValueError("No extractable text found in DOCX")

    return full_text
