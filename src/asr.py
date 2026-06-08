import time

import whisper

from .config import settings
from .exceptions import ASRError
from .utils import add_log


class WhisperASR:
    def __init__(self):
        try:
            self.model = whisper.load_model(settings.whisper_model)
        except Exception as exc:
            raise ASRError("Whisper 模型加载失败") from exc

    def transcribe(self, audio_path: str, source_lang: str, logs: list) -> tuple[str, float]:
        if self.model is None:
            raise ASRError("Whisper 模型未加载")

        add_log(logs, f"Starting ASR on {audio_path} with source language '{source_lang}'.")
        options = {
            "language": None if source_lang == "auto" else source_lang,
            "task": "transcribe",
        }
        start = time.perf_counter()
        try:
            result = self.model.transcribe(audio_path, **options)
        except Exception as exc:
            raise ASRError("ASR 识别失败") from exc
        duration = time.perf_counter() - start
        text = result.get("text", "").strip()
        add_log(logs, f"ASR completed in {duration:.2f}s. Recognized text length: {len(text)}.")
        return text, duration
