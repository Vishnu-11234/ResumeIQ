
from .resume_extractor import extract_resume
from .employment_history_extractor import extract_employment_history
from .experience_calculator import calculate_experience

from ..llm.model_manager import model_manager
from ..llm.inference import generate_resume_output
from ..llm.output_parser import parse_resume_output


def _is_reliable_employment_history(records: list[dict]) -> bool:
    """
    Perform basic validation before trusting the
    deterministic experience calculation.

    This is a structural validation, not a guarantee
    that every extracted record is factually correct.
    """

    if not records:
        return False

    for record in records:
        if not isinstance(record, dict):
            return False

        if not record.get("job_title"):
            return False

        if not record.get("start_date"):
            return False

        if "end_date" not in record:
            return False

        if not record.get("source_text"):
            return False

    return True


def parse_resume(resume_path: str) -> dict:
    """
    Complete resume extraction and structured parsing pipeline.

    Pipeline:
        1. Extract and preprocess resume text.
        2. Generate structured information using Qwen.
        3. Validate the Qwen output.
        4. Extract employment history.
        5. Calculate total professional experience.
        6. Assemble the final response.
    """

    # --------------------------------------------------
    # STEP 1: Extract and preprocess resume text
    # --------------------------------------------------

    extracted_resume = extract_resume(resume_path)

    cleaned_text = extracted_resume["cleaned_text"]


    # --------------------------------------------------
    # STEP 2: Load the fine-tuned Qwen model
    # --------------------------------------------------

    tokenizer, model = model_manager.get_model()


    # --------------------------------------------------
    # STEP 3: Generate structured JSON
    # --------------------------------------------------

    generated_output = generate_resume_output(
        resume_text=cleaned_text,
        tokenizer=tokenizer,
        model=model
    )


    # --------------------------------------------------
    # STEP 4: Parse and validate Qwen output
    # --------------------------------------------------

    structured_data = parse_resume_output(generated_output)


    # --------------------------------------------------
    # STEP 5: Extract employment history
    # --------------------------------------------------

    employment_history = extract_employment_history(
        cleaned_text
    )


    # --------------------------------------------------
    # STEP 6: Calculate professional experience
    # --------------------------------------------------

    experience_calculation = None

    if _is_reliable_employment_history(employment_history):

        experience_calculation = calculate_experience(
            employment_history
        )

        # Replace Qwen's estimate only when we have
        # structurally valid employment records.
        structured_data["years_experience"] = (
            experience_calculation["total_experience_years"]
        )


    # --------------------------------------------------
    # STEP 7: Return final response
    # --------------------------------------------------

    return {
        "file_name": extracted_resume["file_name"],
        "resume_data": structured_data,
        "employment_history": employment_history,
        "experience_calculation": experience_calculation
    }
