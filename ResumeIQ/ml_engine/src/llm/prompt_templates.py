
"""
Prompt templates for ResumeIQ resume information extraction.

The prompts intentionally follow the format used in the
Qwen fine-tuning dataset.
"""


SYSTEM_PROMPT = (
    "You are an expert resume parser. "
    "Extract structured information from resumes and return ONLY valid JSON. "
    "Do not include explanations or extra text."
)


USER_PROMPT_TEMPLATE = """Resume:
{resume_text}"""


def build_messages(resume_text: str) -> list[dict]:
    """
    Build chat messages for the fine-tuned Qwen model.

    Args:
        resume_text: Cleaned resume text.

    Returns:
        A list containing system and user messages.
    """

    if not isinstance(resume_text, str):
        raise TypeError("Resume text must be a string")

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty")

    user_prompt = USER_PROMPT_TEMPLATE.format(
        resume_text=resume_text
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    return messages
