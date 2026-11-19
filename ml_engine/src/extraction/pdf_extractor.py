
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Provided file is not a PDF")

    try:
        reader = PdfReader(str(path))

        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported")

        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            page_text = (page.extract_text() or "").strip()

            if page_text:
                extracted_pages.append(
                    f"--- Page {page_number} ---\n{page_text}"
                )

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract PDF text: {error}"
        ) from error

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise ValueError(
            "No extractable text found. PDF may be scanned or empty."
        )

    return full_text
