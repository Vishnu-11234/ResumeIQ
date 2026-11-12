
import re


# Maps different names of the same skill to a canonical name.
SKILL_ALIASES = {
    "postgres": "postgresql",
    "postgresql": "postgresql",

    "js": "javascript",
    "javascript": "javascript",

    "ml": "machine learning",
    "machine learning": "machine learning",

    "rest apis": "rest api",
    "rest api": "rest api",

    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",

    "reactjs": "react",
    "react.js": "react",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
}


def normalize_skill(skill: str) -> str:
    """
    Convert a skill name into its canonical representation.
    """

    if not isinstance(skill, str):
        raise TypeError("Skill must be a string")

    # Remove leading/trailing spaces, lowercase and
    # collapse consecutive whitespace.
    skill = re.sub(r"\s+", " ", skill.strip().lower())

    if not skill:
        raise ValueError("Skill cannot be empty")

    # Return the canonical name if an alias exists.
    return SKILL_ALIASES.get(skill, skill)


def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize a list of skills and remove duplicates.
    """

    normalized = []

    for skill in skills:
        canonical_skill = normalize_skill(skill)

        if canonical_skill not in normalized:
            normalized.append(canonical_skill)

    return normalized
