
from sentence_transformers import SentenceTransformer
from .skill_normalizer import normalize_skill

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model


def semantic_match_skills(
    resume_skills,
    required_skills,
    preferred_skills,
    threshold=0.75
):
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1")

    resume = list(dict.fromkeys(
        normalize_skill(s) for s in resume_skills
    ))

    required = list(dict.fromkeys(
        normalize_skill(s) for s in required_skills
    ))

    preferred = list(dict.fromkeys(
        normalize_skill(s) for s in preferred_skills
    ))

    targets = required + preferred

    if not resume or not targets:
        return {
            "partial_matches": [],
            "unmatched_required": [
                s for s in required if s not in resume
            ],
            "unmatched_preferred": [
                s for s in preferred if s not in resume
            ]
        }

    model = get_model()

    resume_embeddings = model.encode(
        resume,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    target_embeddings = model.encode(
        targets,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    # Dot product of normalized vectors = cosine similarity.
    similarity_matrix = (
        target_embeddings @ resume_embeddings.T
    )

    # Track exact matches first.
    used_targets = {
        i for i, target in enumerate(targets)
        if target in resume
    }

    used_resume_skills = {
        i for i, candidate in enumerate(resume)
        if candidate in targets
    }

    candidates = []

    for target_index, target in enumerate(targets):

        if target_index in used_targets:
            continue

        for resume_index, candidate in enumerate(resume):

            if resume_index in used_resume_skills:
                continue

            score = similarity_matrix[
                target_index, resume_index
            ].item()

            if score >= threshold:
                candidates.append(
                    (score, target_index, resume_index)
                )

    # Highest similarity pairs get priority.
    candidates.sort(reverse=True)

    partial_matches = []

    for score, target_index, resume_index in candidates:

        if target_index in used_targets:
            continue

        if resume_index in used_resume_skills:
            continue

        used_targets.add(target_index)
        used_resume_skills.add(resume_index)

        partial_matches.append({
            "job_skill": targets[target_index],
            "candidate_skill": resume[resume_index],
            "similarity": round(score, 4)
        })

    unmatched_required = [
        skill
        for i, skill in enumerate(required)
        if i not in used_targets
    ]

    unmatched_preferred = [
        skill
        for i, skill in enumerate(preferred)
        if len(required) + i not in used_targets
    ]

    return {
        "partial_matches": partial_matches,
        "unmatched_required": unmatched_required,
        "unmatched_preferred": unmatched_preferred
    }
