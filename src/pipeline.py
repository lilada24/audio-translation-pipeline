import os
import time
import traceback

import gradio as gr

from .asr import WhisperASR
from .config import settings
from .exceptions import PipelineError
from .translator import BaiduTranslator
from .tts import EdgeTTSEngine
from .utils import add_log, ensure_output_dir


class Pipeline:
    def __init__(self, asr_engine: WhisperASR | None = None, translator: BaiduTranslator | None = None, tts_engine: EdgeTTSEngine | None = None):
        self.asr = asr_engine or WhisperASR()
        self.translator = translator or BaiduTranslator()
        self.tts = tts_engine or EdgeTTSEngine()
        self.output_dir = settings.output_dir

    async def run(self, audio_path, source_lang, target_lang):
        logs: list[str] = []
        ensure_output_dir(self.output_dir)

        if not audio_path:
            raise gr.Error("请先上传 WAV 或 MP3 音频文件。")

        try:
            add_log(logs, "Pipeline started.")
            stage_start = time.perf_counter()

            source_text, asr_time = self.asr.transcribe(audio_path, source_lang, logs)
            if not source_text:
                add_log(logs, "未识别出文本，请确认音频文件是否有效。")

            translated_text, translate_time = await self.translator.translate(source_text or "", source_lang, target_lang, logs)
            output_audio_path, tts_time = await self.tts.synthesize(translated_text, target_lang, logs)

            total_time = time.perf_counter() - stage_start
            add_log(logs, f"Pipeline completed successfully in {total_time:.2f}s.")
            add_log(logs, f"ASR: {asr_time:.2f}s, MT: {translate_time:.2f}s, TTS: {tts_time:.2f}s.")

            return source_text, translated_text, output_audio_path, "\n".join(logs)
        except PipelineError as exc:
            add_log(logs, f"Pipeline failed: {str(exc)}")
            add_log(logs, traceback.format_exc())
            raise gr.Error("流程发生错误，请查看日志或确认音频与语言配置是否正确。") from exc
        except Exception as exc:
            add_log(logs, f"Pipeline failed: {str(exc)}")
            add_log(logs, traceback.format_exc())
            raise gr.Error("流程发生错误，请查看日志或确认音频与语言配置是否正确。") from exc
