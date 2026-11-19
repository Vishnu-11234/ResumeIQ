
import re
import unicodedata


def clean_resume_text(text: str) -> str:
    """
    Clean extracted resume text while preserving its meaning.
    """

    if not isinstance(text, str):
        raise TypeError("Resume text must be a string")

    if not text.strip():
        raise ValueError("Resume text cannot be empty")

    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Remove null characters
    text = text.replace("\x00", "")

    # Remove common PDF extraction artifacts
    text = text.replace("\ufeff", "")
    text = text.replace("\u00a0", " ")

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Limit excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
