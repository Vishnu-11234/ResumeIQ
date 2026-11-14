
from .resume_extractor import extract_resume

from ..llm.model_manager import model_manager
from ..llm.inference import generate_resume_output
from ..llm.output_parser import parse_resume_output


def parse_resume(resume_path: str) -> dict:
    """
    Complete resume extraction and structured parsing pipeline.
    """

    # Step 1: Extract and preprocess resume text
    resume_data = extract_resume(resume_path)

    cleaned_text = resume_data["cleaned_text"]

    # Step 2: Load the fine-tuned model
    tokenizer, model = model_manager.get_model()

    # Step 3: Generate structured JSON text
    generated_output = generate_resume_output(
        resume_text=cleaned_text,
        tokenizer=tokenizer,
        model=model
    )

    # Step 4: Parse and validate model output
    structured_data = parse_resume_output(generated_output)

    return {
        "file_name": resume_data["file_name"],
        "resume_data": structured_data
    }
