from .job_matcher import match_resume_with_job


def validate_ranking_inputs(resume_data, jobs_data, top_n):
    """
    Validate the main inputs of the ranking engine.
    """

    if not isinstance(resume_data, dict):
        raise TypeError("Resume data must be a dictionary")

    if not isinstance(jobs_data, list):
        raise TypeError("Jobs data must be a list")

    if isinstance(top_n, bool) or not isinstance(top_n, int):
        raise TypeError("top_n must be an integer")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero")


def validate_job_metadata(job):
    """
    Validate metadata required to identify and display a job.
    """

    if not isinstance(job, dict):
        raise TypeError("Each job must be a dictionary")

    job_id = job.get("job_id")
    job_title = job.get("job_title")
    company = job.get("company")

    if not isinstance(job_id, str) or not job_id.strip():
        raise ValueError("Job must have a valid job_id")

    if not isinstance(job_title, str) or not job_title.strip():
        raise ValueError("Job must have a valid job_title")

    if company is not None and not isinstance(company, str):
        raise TypeError("Company must be a string or None")

    return job_id.strip()


def build_recommendation(job, match_result):
    """
    Combine job metadata with the matching result from Module 3.
    """

    skills = match_result["skills"]
    experience = match_result["experience"]

    return {
        "job_id": job["job_id"].strip(),
        "job_title": job["job_title"].strip(),
        "company": job.get("company"),

        "match_score": match_result["overall_match_score"],

        "component_scores": match_result["component_scores"],
        "component_weights": match_result["component_weights"],

        "matched_skills": {
            "required": skills["matched_required"],
            "preferred": skills["matched_preferred"]
        },

        "partial_matches": {
            "required": skills["partial_required"],
            "preferred": skills["partial_preferred"]
        },

        "missing_skills": {
            "required": skills["missing_required"],
            "preferred": skills["missing_preferred"]
        },

        "experience": experience,

        "unavailable_components": match_result["unavailable_components"]
    }


def rank_jobs_for_resume(resume_data, jobs_data, top_n=10):
    """
    Rank multiple jobs against one resume.

    Returns the top N jobs based on estimated job-alignment score.
    Invalid jobs are recorded without stopping the entire process.
    """

    # Step 1: Validate ranking inputs
    validate_ranking_inputs(
        resume_data,
        jobs_data,
        top_n
    )

    recommendations = []
    failed_jobs = []
    seen_job_ids = set()

    # Step 2: Process every job
    for job in jobs_data:

        job_id = job.get("job_id") if isinstance(job, dict) else None

        try:
            # Step 3: Validate job metadata
            normalized_job_id = validate_job_metadata(job)

            # Step 4: Prevent duplicate job IDs
            if normalized_job_id in seen_job_ids:
                raise ValueError(
                    f"Duplicate job_id: {normalized_job_id}"
                )

            seen_job_ids.add(normalized_job_id)

            # Step 5: Reuse Module 3
            match_result = match_resume_with_job(
                resume_data,
                job
            )

            # Step 6: Build recommendation
            recommendation = build_recommendation(
                job,
                match_result
            )

            recommendations.append(recommendation)

        except (TypeError, ValueError, KeyError) as error:

            # Step 7: Record invalid job and continue
            failed_jobs.append({
                "job_id": job_id,
                "error": str(error)
            })

    # Step 8: Sort by score, highest first
    # Python's sort is stable, so equal scores retain input order.
    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    # Step 9: Select the top N recommendations
    top_recommendations = recommendations[:top_n]

    # Step 10: Assign ranks after sorting and limiting
    for rank, recommendation in enumerate(
        top_recommendations,
        start=1
    ):
        recommendation["rank"] = rank

    # Step 11: Return final ranking report
    return {
        "total_jobs_received": len(jobs_data),
        "total_jobs_ranked": len(recommendations),
        "total_jobs_failed": len(failed_jobs),
        "top_n": top_n,

        "recommendations": top_recommendations,
        "failed_jobs": failed_jobs
    }