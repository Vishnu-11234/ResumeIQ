
import math


def match_experience(candidate_experience, required_experience):

    # Validate required experience
    if isinstance(required_experience, bool) or not isinstance(required_experience, (int, float)):
        raise TypeError("Required experience must be a number")

    if not math.isfinite(required_experience):
        raise ValueError("Required experience must be finite")

    if required_experience < 0:
        raise ValueError("Required experience cannot be negative")

    # Handle unknown candidate experience
    if candidate_experience is None:
        return {
            "candidate_experience": None,
            "required_experience": required_experience,
            "status": "Experience information unavailable",
            "experience_gap": None
        }

    # Validate candidate experience
    if isinstance(candidate_experience, bool) or not isinstance(candidate_experience, (int, float)):
        raise TypeError("Candidate experience must be a number")

    if not math.isfinite(candidate_experience):
        raise ValueError("Candidate experience must be finite")

    if candidate_experience < 0:
        raise ValueError("Candidate experience cannot be negative")

    # Compare experience
    if required_experience == 0:
        status = "No experience required"

    elif candidate_experience >= required_experience:
        status = "Meets requirement"

    else:
        status = "Below requirement"

    # Calculate experience gap
    experience_gap = max(
        0,
        required_experience - candidate_experience
    )

    return {
        "candidate_experience": candidate_experience,
        "required_experience": required_experience,
        "status": status,
        "experience_gap": round(experience_gap, 2)
    }
