
from datetime import date
from typing import Optional


def parse_month(value: str) -> date:
    """
    Convert YYYY-MM into a date representing the first day
    of that month.
    """
    if not isinstance(value, str):
        raise TypeError("Date must be a string in YYYY-MM format")

    try:
        parsed = date.fromisoformat(f"{value}-01")
    except ValueError as error:
        raise ValueError(
            f"Invalid date: {value}. Expected YYYY-MM format."
        ) from error

    if parsed.strftime("%Y-%m") != value:
        raise ValueError(f"Invalid date format: {value}")

    return parsed


def calculate_experience(
    employment_history: list[dict],
    as_of: Optional[str] = None
) -> dict:
    """
    Calculate total employment experience without
    double-counting overlapping months.

    Each employment record must contain:
        start_date: YYYY-MM
        end_date: YYYY-MM or None

    None end_date means currently employed.
    """

    if not isinstance(employment_history, list):
        raise TypeError("Employment history must be a list")

    if not employment_history:
        return {
            "total_experience_months": 0,
            "total_experience_years": 0.0,
            "approximate": False
        }

    current_date = parse_month(as_of) if as_of else date.today()
    current_month = date(current_date.year, current_date.month, 1)

    periods = []

    for index, job in enumerate(employment_history):
        if not isinstance(job, dict):
            raise TypeError(f"Job at index {index} must be a dictionary")

        if "start_date" not in job:
            raise ValueError(f"Missing start_date in job {index}")

        start = parse_month(job["start_date"])

        end_value = job.get("end_date")

        if end_value is None:
            end = current_month
        else:
            end = parse_month(end_value)

        if start > current_month:
            raise ValueError("Employment start date cannot be in the future")

        if end < start:
            raise ValueError(
                f"End date cannot precede start date in job {index}"
            )

        if end > current_month:
            raise ValueError("Employment end date cannot be in the future")

        # Inclusive month-based calculation
        periods.append((
            start.year * 12 + start.month,
            end.year * 12 + end.month
        ))

    periods.sort()

    merged_periods = []

    for start, end in periods:
        if not merged_periods or start > merged_periods[-1][1] + 1:
            merged_periods.append([start, end])
        else:
            merged_periods[-1][1] = max(
                merged_periods[-1][1], end
            )

    total_months = sum(
        end - start + 1
        for start, end in merged_periods
    )

    return {
        "total_experience_months": total_months,
        "total_experience_years": round(total_months / 12, 2),
        "approximate": True
    }
