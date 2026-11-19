
"""
Main resume intelligence pipeline.

Connects model management, LLM inference,
and structured output validation.
"""

from .model_manager import model_manager
from .inference import generate_resume_output
from .output_parser import parse_resume_output


def analyze_resume(
    resume_text: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.1
) -> dict:
    """
    Analyze resume text and return validated structured information.

    Args:
        resume_text: Extracted and cleaned resume text.
        max_new_tokens: Maximum number of generated tokens.
        temperature: Controls generation randomness.

    Returns:
        A validated dictionary containing resume information.
    """

    # Step 1: Get the shared model and tokenizer.
    tokenizer, model = model_manager.get_model()

    # Step 2: Generate structured information using the LLM.
    generated_text = generate_resume_output(
        resume_text=resume_text,
        tokenizer=tokenizer,
        model=model,
        max_new_tokens=max_new_tokens,
        temperature=temperature
    )

    # Step 3: Parse and validate the generated JSON.
    resume_data = parse_resume_output(generated_text)

    # Step 4: Return validated structured data.
    return resume_data
