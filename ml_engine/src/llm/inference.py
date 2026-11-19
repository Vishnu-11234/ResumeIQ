
"""
Inference module for ResumeIQ.

Responsible for generating structured resume information
using the fine-tuned Qwen model.
"""

from threading import Lock

from .prompt_templates import build_messages


# Prevent simultaneous model generation within this process.
_inference_lock = Lock()


def generate_resume_output(
    resume_text: str,
    tokenizer,
    model,
    max_new_tokens: int = 1024,
    temperature: float = 0.1
) -> str:
    """
    Generate structured resume information.
    """

    # 1. Validate inputs
    if not isinstance(resume_text, str):
        raise TypeError("Resume text must be a string")

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty")

    if isinstance(max_new_tokens, bool) or not isinstance(max_new_tokens, int):
        raise TypeError("max_new_tokens must be an integer")

    if max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be greater than zero")

    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
        raise TypeError("temperature must be a number")

    if not 0 <= temperature <= 2:
        raise ValueError("temperature must be between 0 and 2")

    # 2. Import PyTorch only when inference is requested
    import torch

    # 3. Build chat messages
    messages = build_messages(resume_text)

    # 4. Convert messages into Qwen chat format
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True
    )

    # 5. Move input tensors to the model's input device
    input_device = model.get_input_embeddings().weight.device

    inputs = {
        key: value.to(input_device)
        for key, value in inputs.items()
    }

    # 6. Configure generation
    generation_kwargs = {
        "max_new_tokens": max_new_tokens,
        "do_sample": temperature > 0,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id
    }

    if temperature > 0:
        generation_kwargs["temperature"] = temperature

    # 7. Generate output safely
    with _inference_lock:
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                **generation_kwargs
            )

    # 8. Remove input tokens from generated sequence
    input_length = inputs["input_ids"].shape[1]

    generated_ids = output_ids[0][input_length:]

    # 9. Decode generated tokens
    generated_text = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True
    )

    return generated_text.strip()
