
import re
import unicodedata


def normalize_resume_text(text: str) -> str:
    """
    Normalize resume text for consistent downstream processing.
    """

    if not isinstance(text, str):
        raise TypeError("Resume text must be a string")

    if not text.strip():
        raise ValueError("Resume text cannot be empty")

    # Normalize Unicode representation
    text = unicodedata.normalize("NFKC", text)

    # Convert text to lowercase
    text = text.lower()

    # Normalize different dash characters
    text = re.sub(r"[‐‑‒–—]", "-", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Limit excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
