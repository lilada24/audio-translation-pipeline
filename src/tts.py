import asyncio
import os
import time
import uuid

import edge_tts

from .config import settings
from .exceptions import TTSError
from .utils import add_log

VOICE_MAP = {
    "en": "en-US-GuyNeural",
    "zh": "zh-CN-XiaoxiaoNeural",
    "ja": "ja-JP-NanamiNeural",
    "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "it": "it-IT-ElsaNeural",
    "ko": "ko-KR-SunHiNeural",
    "pt": "pt-BR-DanielNeural",
    "ru": "ru-RU-DariyaNeural",
}


class EdgeTTSEngine:
    async def synthesize(self, text: str, target_lang: str, logs: list) -> tuple[str, float]:
        voice = VOICE_MAP.get(target_lang, "en-US-GuyNeural")
        output_filename = f"translated_{uuid.uuid4().hex[:8]}.mp3"
        output_path = os.path.join(settings.output_dir, output_filename)

        add_log(logs, f"Starting TTS using voice '{voice}' and saving to {output_path}.")
        start = time.perf_counter()
        try:
            await self._save_audio(text, voice, output_path)
        except Exception as exc:
            raise TTSError("TTS 合成失败") from exc
        duration = time.perf_counter() - start
        add_log(logs, f"TTS completed in {duration:.2f}s.")
        return output_path, duration

    async def _save_audio(self, text: str, voice: str, output_path: str):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
