
import os

import httpx


AI_ENGINE_URL = os.getenv(
    "AI_ENGINE_URL",
    "http://127.0.0.1:8001"
)

AI_ENGINE_TIMEOUT = 120.0


class AIEngineConnectionError(Exception):
    """Raised when the backend cannot communicate with the AI Engine."""


class AIEngineResponseError(Exception):
    """Raised when the AI Engine returns an unsuccessful response."""


async def analyze_resume_text(resume_text: str) -> dict:
    """
    Send extracted resume text to the AI Engine
    and return the structured analysis.
    """

    url = f"{AI_ENGINE_URL}/analyze"

    try:
        async with httpx.AsyncClient(
            timeout=AI_ENGINE_TIMEOUT
        ) as client:

            response = await client.post(
                url,
                json={"resume_text": resume_text}
            )

            response.raise_for_status()

            return response.json()

    except httpx.TimeoutException as error:
        raise AIEngineConnectionError(
            "AI Engine took too long to respond."
        ) from error

    except httpx.RequestError as error:
        raise AIEngineConnectionError(
            "Could not connect to AI Engine."
        ) from error

    except httpx.HTTPStatusError as error:
        raise AIEngineResponseError(
            f"AI Engine returned HTTP {error.response.status_code}."
        ) from error
