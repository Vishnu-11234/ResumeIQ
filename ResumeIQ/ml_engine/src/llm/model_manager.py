
from threading import Lock

from .model_loader import load_model


class ModelManager:

    def __init__(self):
        self._tokenizer = None
        self._model = None
        self._lock = Lock()

    def get_model(self):
        """
        Return the loaded model.

        Load it only once, then reuse it.
        """

        # Fast path: model already loaded.
        if self._model is not None:
            return self._tokenizer, self._model

        # Only one thread can initialize the model.
        with self._lock:

            # Check again after acquiring the lock.
            if self._model is None:

                tokenizer, model = load_model()

                # Store only after successful loading.
                self._tokenizer = tokenizer
                self._model = model

        return self._tokenizer, self._model


# Shared manager instance.
model_manager = ModelManager()
