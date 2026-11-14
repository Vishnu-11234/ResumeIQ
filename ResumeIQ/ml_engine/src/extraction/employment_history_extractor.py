
import re
from datetime import datetime
from typing import Optional


# --------------------------------------------------
# 1. DATE PATTERNS
# --------------------------------------------------

MONTH_PATTERN = (
    r"January|February|March|April|May|June|July|August|"
    r"September|October|November|December"
)

# Example: July 2011 to November 2012
DATE_RANGE_PATTERN = re.compile(
    rf"\b({MONTH_PATTERN})\s+(\d{{4}})"
    rf"\s*(?:to|[-–—])\s*"
    rf"({MONTH_PATTERN})\s+(\d{{4}})\b",
    re.IGNORECASE
)

# Example: 05/2014 to 06/2015
# Also supports: 05/2014 to Current
NUMERIC_DATE_RANGE_PATTERN = re.compile(
    r"\b(\d{1,2})/(\d{4})\s*"
    r"(?:to|[-–—])\s*"
    r"(Current|\d{1,2}/\d{4})\b",
    re.IGNORECASE
)


# --------------------------------------------------
# 2. SECTION HEADINGS
# --------------------------------------------------

EXPERIENCE_HEADINGS = {
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "career history",
    "professional history",
    "work history",
    "career experience",
    "employment experience",
}

STOP_HEADINGS = {
    "education",
    "academic qualifications",
    "certifications",
    "certificates",
    "skills",
    "technical skills",
    "projects",
    "interests",
    "references",
    "accomplishments",
}


# --------------------------------------------------
# 3. IGNORED LINES
# --------------------------------------------------

IGNORED_LINES = {
    "company name",
    "city",
    "state",
    "country",
    "usa",
    "to",
    "current",
}


# --------------------------------------------------
# 4. DATE CONVERSION
# --------------------------------------------------

def _month_to_iso(month: str, year: str) -> str:
    parsed = datetime.strptime(
        f"{month} {year}",
        "%B %Y"
    )
    return parsed.strftime("%Y-%m")


def _parse_numeric_date(month: str, year: str) -> str:
    month = int(month)
    year = int(year)

    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}")

    return f"{year:04d}-{month:02d}"


# --------------------------------------------------
# 5. EXPERIENCE SECTION DETECTION
# --------------------------------------------------

def _find_experience_section(text: str) -> str:
    lines = text.splitlines()

    start_index = None
    end_index = len(lines)

    for index, line in enumerate(lines):
        heading = line.strip().lower().rstrip(":")
        if heading in EXPERIENCE_HEADINGS:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    for index in range(start_index, len(lines)):
        heading = lines[index].strip().lower().rstrip(":")
        if heading in STOP_HEADINGS:
            end_index = index
            break

    return "\n".join(lines[start_index:end_index])


# --------------------------------------------------
# 6. JOB TITLE EXTRACTION
# --------------------------------------------------

def _find_job_title(
    text_before_date: str,
    text_after_date: str
) -> Optional[str]:

    def find_candidate(text: str) -> Optional[str]:

        lines = text.splitlines()

        for line in lines:
            candidate = line.strip()
            if not candidate:
                continue

            normalized = candidate.lower().strip(" :,-")

            if normalized in IGNORED_LINES:
                continue

            if DATE_RANGE_PATTERN.search(candidate):
                continue

            if NUMERIC_DATE_RANGE_PATTERN.search(candidate):
                continue

            if re.fullmatch(r"\d{4}", candidate):
                continue

            if normalized in EXPERIENCE_HEADINGS | STOP_HEADINGS:
                continue

            if len(candidate) > 100:
                continue

            return candidate

        return None

    # Prefer the title immediately before the date.
    preceding_lines = text_before_date.splitlines()
    preceding_lines.reverse()

    title = find_candidate("\n".join(preceding_lines))

    if title:
        return title

    # Fall back to the text following the date.
    return find_candidate(text_after_date)


# --------------------------------------------------
# 7. EMPLOYMENT HISTORY EXTRACTION
# --------------------------------------------------

def extract_employment_history(resume_text: str) -> list[dict]:

    if not isinstance(resume_text, str):
        raise TypeError("Resume text must be a string")

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty")

    experience_text = _find_experience_section(resume_text)

    if not experience_text.strip():
        return []

    # Collect both date formats.
    matches = []

    for match in DATE_RANGE_PATTERN.finditer(experience_text):
        matches.append(("named", match))

    for match in NUMERIC_DATE_RANGE_PATTERN.finditer(experience_text):
        matches.append(("numeric", match))

    # Maintain original document order.
    matches.sort(key=lambda item: item[1].start())

    records = []

    for index, (date_type, match) in enumerate(matches):

        if date_type == "named":

            start_date = _month_to_iso(
                match.group(1),
                match.group(2)
            )

            end_date = _month_to_iso(
                match.group(3),
                match.group(4)
            )

        else:

            start_date = _parse_numeric_date(
                match.group(1),
                match.group(2)
            )

            end_value = match.group(3)

            if end_value.lower() == "current":
                end_date = None
            else:
                end_month, end_year = end_value.split("/")

                end_date = _parse_numeric_date(
                    end_month,
                    end_year
                )

        if end_date is not None and start_date > end_date:
            continue

        next_match_start = (
            matches[index + 1][1].start()
            if index + 1 < len(matches)
            else len(experience_text)
        )

        text_before_date = experience_text[:match.start()]

        text_after_date = experience_text[
            match.end():next_match_start
        ]

        job_title = _find_job_title(
            text_before_date,
            text_after_date
        )

        records.append({
            "job_title": job_title,
            "start_date": start_date,
            "end_date": end_date,
            "source_text": match.group(0)
        })

    return records
