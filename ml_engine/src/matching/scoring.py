
import math

from .skill_normalizer import normalize_skill


def calculate_match_score(
    skill_result,
    semantic_result,
    experience_result,
    required_skills,
    preferred_skills
):
    """
    Calculate ResumeIQ estimated job-alignment score.
    """

    # Initial scoring weights
    weights = {
        "required_skills": 0.45,
        "preferred_skills": 0.10,
        "semantic_matching": 0.15,
        "experience": 0.30
    }

    # Validate skill lists
    if not isinstance(required_skills, list):
        raise TypeError("Required skills must be a list")

    if not isinstance(preferred_skills, list):
        raise TypeError("Preferred skills must be a list")

    # Normalize and remove duplicate skills
    required_skills = set(
        normalize_skill(skill) for skill in required_skills
    )

    preferred_skills = set(
        normalize_skill(skill) for skill in preferred_skills
    )

    # Extract matching results
    matched_required = skill_result["matched_required"]
    matched_preferred = skill_result["matched_preferred"]

    partial_matches = semantic_result["partial_matches"]

    # Validate matching result structures
    if not isinstance(partial_matches, list):
        raise TypeError("Partial matches must be a list")

    if not isinstance(matched_required, list):
        raise TypeError("Matched required skills must be a list")

    if not isinstance(matched_preferred, list):
        raise TypeError("Matched preferred skills must be a list")

    # Validate exact matches
    for skill in matched_required + matched_preferred:
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError("Invalid exact skill match")

    # Normalize exact matches
    matched_required = set(
        normalize_skill(skill) for skill in matched_required
    )

    matched_preferred = set(
        normalize_skill(skill) for skill in matched_preferred
    )

    # Required skill score
    required_score = (
        len(matched_required.intersection(required_skills))
        / len(required_skills) * 100
        if required_skills else None
    )

    # Preferred skill score
    preferred_score = (
        len(matched_preferred.intersection(preferred_skills))
        / len(preferred_skills) * 100
        if preferred_skills else None
    )

    # Semantic coverage score
    total_job_skills = (
        len(required_skills) + len(preferred_skills)
    )

    exact_matches = matched_required.union(matched_preferred)

    # Store the highest valid partial similarity
    # for each unique job skill
    partial_credit = {}

    for match in partial_matches:

        if not isinstance(match, dict):
            raise TypeError("Each partial match must be a dictionary")

        job_skill = match.get("job_skill")
        candidate_skill = match.get("candidate_skill")
        similarity = match.get("similarity")

        if not isinstance(job_skill, str) or not job_skill.strip():
            raise ValueError("Invalid job skill in partial match")

        if not isinstance(candidate_skill, str) or not candidate_skill.strip():
            raise ValueError("Invalid candidate skill in partial match")

        if (
            isinstance(similarity, bool)
            or not isinstance(similarity, (int, float))
        ):
            raise TypeError("Similarity must be a number")

        if not math.isfinite(similarity):
            raise ValueError("Similarity must be finite")

        if not 0 <= similarity <= 1:
            raise ValueError("Similarity must be between 0 and 1")

        normalized_job_skill = normalize_skill(job_skill)

        # Ignore skills that are not part of this job
        if normalized_job_skill not in required_skills.union(preferred_skills):
            continue

        # Exact matches must not receive additional partial credit
        if normalized_job_skill in exact_matches:
            continue

        # Prevent duplicate partial matches from inflating the score
        partial_credit[normalized_job_skill] = max(
            partial_credit.get(normalized_job_skill, 0),
            similarity
        )

    semantic_credit = (
        len(exact_matches.intersection(
            required_skills.union(preferred_skills)
        ))
        + sum(partial_credit.values())
    )

    semantic_score = (
        semantic_credit / total_job_skills * 100
        if total_job_skills else None
    )

    # Experience score
    candidate_experience = experience_result[
        "candidate_experience"
    ]

    required_experience = experience_result[
        "required_experience"
    ]

    if required_experience == 0:
        experience_score = 100

    elif candidate_experience is None:
        experience_score = None

    else:
        experience_score = min(
            candidate_experience / required_experience * 100,
            100
        )

    # Collect component scores
    component_scores = {
        "required_skills": required_score,
        "preferred_skills": preferred_score,
        "semantic_matching": semantic_score,
        "experience": experience_score
    }

    # Validate calculated component scores
    for name, score in component_scores.items():

        if score is None:
            continue

        if not math.isfinite(score):
            raise ValueError(f"{name} score must be finite")

        if not 0 <= score <= 100:
            raise ValueError(f"{name} score must be between 0 and 100")

    # Keep only available components
    active_weights = {
        name: weights[name]
        for name, score in component_scores.items()
        if score is not None
    }

    total_active_weight = sum(active_weights.values())

    # Prevent division by zero
    if total_active_weight == 0:
        raise ValueError(
            "Cannot calculate score: no scoring components available"
        )

    # Calculate final weighted score
    final_score = sum(
        component_scores[name] * weight
        for name, weight in active_weights.items()
    ) / total_active_weight

    # Normalize active weights
    normalized_weights = {
        name: round(weight / total_active_weight, 4)
        for name, weight in active_weights.items()
    }

    return {
        "overall_match_score": round(final_score, 2),

        "component_scores": {
            name: round(score, 2)
            for name, score in component_scores.items()
            if score is not None
        },

        "component_weights": normalized_weights,

        "unavailable_components": [
            name
            for name, score in component_scores.items()
            if score is None
        ]
    }
