class PipelineError(Exception):
    """Pipeline 层基础异常。"""

    def __init__(self, message: str, original_exception: Exception | None = None):
        super().__init__(message)
        self.original = original_exception


class ASRError(PipelineError):
    """ASR 服务异常。"""


class TranslationError(PipelineError):
    """翻译服务异常。"""


class TTSError(PipelineError):
    """TTS 服务异常。"""
