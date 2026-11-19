
from pathlib import Path
import json


# --------------------------------------------------
# Model configuration
# --------------------------------------------------

BASE_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

ADAPTER_PATH = (
    Path(__file__).resolve().parents[2] / "trained_model"
)


# --------------------------------------------------
# Load tokenizer and model
# --------------------------------------------------

def load_model():

    # 1. Validate adapter directory
    if not ADAPTER_PATH.exists():
        raise FileNotFoundError(
            f"Adapter directory not found: {ADAPTER_PATH}"
        )

    config_path = ADAPTER_PATH / "adapter_config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Adapter configuration not found: {config_path}"
        )

    # 2. Verify that adapter belongs to the expected base model
    with open(config_path, "r", encoding="utf-8") as file:
        adapter_config = json.load(file)

    adapter_base_model = adapter_config.get(
        "base_model_name_or_path"
    )

    if adapter_base_model != BASE_MODEL_NAME:
        raise ValueError(
            f"Base model mismatch. Expected {BASE_MODEL_NAME}, "
            f"but adapter uses {adapter_base_model}"
        )

    # 3. Import heavy dependencies only when loading is requested
    try:
        import torch
        from transformers import (
            AutoTokenizer,
            AutoModelForCausalLM,
            BitsAndBytesConfig
        )
        from peft import PeftModel

    except ImportError as error:
        raise ImportError(
            f"Required model-loading dependency is missing: {error}"
        ) from error

    # 4. Check GPU availability
    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU is unavailable. "
            "Use a compatible GPU environment such as Google Colab."
        )

    # 5. Configure 4-bit NF4 quantization
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )

    # 6. Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        str(ADAPTER_PATH)
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 7. Load original pretrained model
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        quantization_config=quantization_config,
        device_map="auto",
        low_cpu_mem_usage=True
    )

    # 8. Attach trained LoRA adapter
    model = PeftModel.from_pretrained(
        base_model,
        str(ADAPTER_PATH),
        is_trainable=False
    )

    # 9. Switch to inference mode
    model.eval()

    return tokenizer, model
