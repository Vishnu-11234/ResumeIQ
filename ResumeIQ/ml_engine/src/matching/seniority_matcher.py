# Standard seniority hierarchy.
# A higher number means a higher seniority level.

SENIORITY_LEVELS = {
    "intern": 0,
    "junior": 1,
    "entry-level": 1,
    "mid-level": 2,
    "mid": 2,
    "senior": 3,
    "lead": 4,
    "principal": 5,
    "manager": 5,
    "director": 6
}


def normalize_seniority(seniority):
    """
    Normalize a seniority label.
    """

    if not isinstance(seniority, str):
        raise TypeError(
            "Seniority must be a string"
        )

    normalized = seniority.strip().lower()

    if not normalized:
        raise ValueError(
            "Seniority cannot be empty"
        )

    if normalized not in SENIORITY_LEVELS:
        raise ValueError(
            f"Unknown seniority level: {seniority}"
        )

    return normalized


def match_seniority(
    candidate_seniority,
    required_seniority
):
    """
    Compare candidate seniority with required job seniority.
    """

    candidate = normalize_seniority(
        candidate_seniority
    )

    required = normalize_seniority(
        required_seniority
    )

    candidate_level = SENIORITY_LEVELS[
        candidate
    ]

    required_level = SENIORITY_LEVELS[
        required
    ]

    if candidate_level == required_level:
        status = "Meets requirement"

    elif candidate_level > required_level:
        status = "Above requirement"

    else:
        status = "Below requirement"

    level_difference = (
        candidate_level - required_level
    )

    return {
        "candidate_seniority": candidate,
        "required_seniority": required,
        "candidate_level": candidate_level,
        "required_level": required_level,
        "level_difference": level_difference,
        "status": status
    }