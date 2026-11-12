
from .skill_matcher import match_skills
from .skill_normalizer import normalize_skill
from .experience_matcher import match_experience
from .semantic_matcher import semantic_match_skills
from .scoring import calculate_match_score


def validate_skill_list(skills, field_name):

    if not isinstance(skills, list):
        raise TypeError(
            f"{field_name} must be a list"
        )

    for skill in skills:

        if not isinstance(skill, str):
            raise TypeError(
                f"Every item in {field_name} must be a string"
            )

        if not skill.strip():
            raise ValueError(
                f"{field_name} cannot contain empty skill names"
            )




def validate_no_overlapping_skills(required_skills, preferred_skills):

    required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    preferred = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    overlapping_skills = required.intersection(preferred)

    if overlapping_skills:
        raise ValueError(
            f"Skills cannot appear in both required and preferred lists: "
            f"{sorted(overlapping_skills)}"
        )



def match_resume_with_job(resume_data, job_data):
    """
    Orchestrate the complete ResumeIQ matching workflow.

    Expected resume_data:
        {
            "skills": ["Python", "Machine Learning"],
            "total_experience": 1.5
        }

    Expected job_data:
        {
            "required_skills": ["Python", "Machine Learning"],
            "preferred_skills": ["Docker"],
            "minimum_experience": 2
        }
    """

    # 1. Validate input structure
    if not isinstance(resume_data, dict):
        raise TypeError("Resume data must be a dictionary")

    if not isinstance(job_data, dict):
        raise TypeError("Job data must be a dictionary")

    required_resume_fields = [
        "skills",
        "total_experience"
    ]

    required_job_fields = [
        "required_skills",
        "preferred_skills",
        "minimum_experience"
    ]

    for field in required_resume_fields:
        if field not in resume_data:
            raise ValueError(f"Missing resume field: {field}")

    for field in required_job_fields:
        if field not in job_data:
            raise ValueError(f"Missing job field: {field}")

    # 2. Extract input data
   # 2. Extract input data
    resume_skills = resume_data["skills"]

    required_skills = job_data["required_skills"]
    preferred_skills = job_data["preferred_skills"]

    # 3. Validate skill lists
    validate_skill_list(
        resume_skills,
        "resume skills"
    )

    validate_skill_list(
        required_skills,
        "required skills"
    )

    validate_skill_list(
        preferred_skills,
        "preferred skills"
    )

    validate_no_overlapping_skills(
    required_skills,
    preferred_skills
    )

    candidate_experience = resume_data["total_experience"]
    required_experience = job_data["minimum_experience"]

    # 3. Exact skill matching
    skill_result = match_skills(
        resume_skills,
        required_skills,
        preferred_skills
    )

    # 4. Semantic skill matching
    semantic_result = semantic_match_skills(
        resume_skills,
        required_skills,
        preferred_skills
    )

    # 5. Experience matching
    experience_result = match_experience(
        candidate_experience,
        required_experience
    )

    # 6. Calculate overall matching score
    score_result = calculate_match_score(
        skill_result,
        semantic_result,
        experience_result,
        required_skills,
        preferred_skills
    )

    # 7. Separate exact and partial matches
    partial_matches = semantic_result["partial_matches"]

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
    }

    preferred_set = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    partial_required = [
        match for match in partial_matches
        if match["job_skill"] in required_set
    ]

    partial_preferred = [
        match for match in partial_matches
        if match["job_skill"] in preferred_set
    ]

    # 8. Build the final matching report
    return {
        "overall_match_score": score_result[
            "overall_match_score"
        ],

        "component_scores": score_result[
            "component_scores"
        ],

        "component_weights": score_result[
            "component_weights"
        ],

        "unavailable_components": score_result[
            "unavailable_components"
        ],

        "skills": {
            "matched_required": skill_result[
                "matched_required"
            ],

            "matched_preferred": skill_result[
                "matched_preferred"
            ],

            "partial_required": partial_required,

            "partial_preferred": partial_preferred,

            "missing_required": semantic_result[
                "unmatched_required"
            ],

            "missing_preferred": semantic_result[
                "unmatched_preferred"
            ]
        },

        "experience": experience_result
    }
