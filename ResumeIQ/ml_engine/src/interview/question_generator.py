"""
Interview Question Generator

Version 1:
Rule-based interview question generation from
resume and job description.
"""


class InterviewQuestionGenerator:
    """Generate interview questions from resume and job description."""

    def __init__(self):
        self.skill_keywords = [
            "python",
            "java",
            "c++",
            "sql",
            "machine learning",
            "deep learning",
            "nlp",
            "rest api",
            "apis",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "docker",
            "git",
            "aws",
        ]

    def extract_skills(self, text):
        """Extract known technical skills from text."""

        text = text.lower()

        found_skills = []

        for skill in self.skill_keywords:
            if skill in text:
                found_skills.append(skill)

        return found_skills

    def generate_questions(self, resume_text, job_description):
        """Generate interview questions from resume and JD."""

        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(job_description)

        questions = {
            "technical": [],
            "resume_based": [],
            "job_description": [],
            "behavioral": [],
        }

        # Technical questions based on resume skills
        for skill in resume_skills:
            questions["technical"].append(
                f"How have you used {skill} in your projects?"
            )

        # Resume-based questions
        if resume_skills:
            questions["resume_based"].append(
                f"Explain your experience with {resume_skills[0]} "
                "and describe one project where you used it."
            )

        questions["resume_based"].append(
            "Tell me about your most important project mentioned in your resume."
        )

        questions["resume_based"].append(
            "What was your specific contribution to the project?"
        )

        # Questions based on JD requirements
        for skill in jd_skills:
            questions["job_description"].append(
                f"The job requires {skill}. How would you demonstrate "
                f"your experience with {skill}?"
            )

        # Behavioral questions
        questions["behavioral"].append(
            "Tell me about a challenging situation you faced in a project."
        )

        questions["behavioral"].append(
            "How do you handle problems when working under pressure?"
        )

        return questions


if __name__ == "__main__":

    resume = """
    Python developer with experience in Machine Learning and NLP.
    Built a Resume Screening System using Python, NLP and SQL.
    """

    job_description = """
    We are looking for a Python developer with knowledge of
    Machine Learning, NLP, SQL and REST APIs.
    """

    generator = InterviewQuestionGenerator()

    result = generator.generate_questions(
        resume,
        job_description
    )

    print("\n===== INTERVIEW QUESTIONS =====\n")

    for category, questions in result.items():

        print(f"\n--- {category.upper()} ---")

        for index, question in enumerate(questions, start=1):
            print(f"{index}. {question}")