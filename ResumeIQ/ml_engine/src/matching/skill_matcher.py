
from .skill_normalizer import normalize_skills


def match_skills(resume_skills, required_skills, preferred_skills):
    """
    Compare resume skills with required and preferred job skills.
    """

    resume = set(normalize_skills(resume_skills))
    required = set(normalize_skills(required_skills))
    preferred = set(normalize_skills(preferred_skills))

    matched_required = resume.intersection(required)
    missing_required = required - resume

    matched_preferred = resume.intersection(preferred)
    missing_preferred = preferred - resume

    return {
        "matched_required": sorted(matched_required),
        "missing_required": sorted(missing_required),
        "matched_preferred": sorted(matched_preferred),
        "missing_preferred": sorted(missing_preferred)
    }
