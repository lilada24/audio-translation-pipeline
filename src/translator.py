import hashlib
import random
import time

import aiohttp

from .config import settings
from .exceptions import TranslationError
from .utils import add_log

BAIDU_LANGUAGE_CODE_MAP = {
    "auto": "auto",
    "en": "en",
    "zh": "zh",
    "ja": "jp",
    "es": "spa",
    "fr": "fra",
    "de": "de",
    "it": "it",
    "ko": "kor",
    "pt": "pt",
    "ru": "ru",
}


class BaiduTranslator:
    async def translate(self, source_text: str, source_lang: str, target_lang: str, logs: list) -> tuple[str, float]:
        add_log(
            logs,
            f"Starting translation from '{source_lang}' to '{target_lang}'.",
        )
        start = time.perf_counter()

        if not settings.baidu_translate_app_id or not settings.baidu_translate_secret_key:
            raise TranslationError(
                "百度翻译API密钥未配置，请在 .env 文件或环境变量中设置 BAIDU_TRANSLATE_APP_ID 和 BAIDU_TRANSLATE_SECRET_KEY"
            )

        source_code = BAIDU_LANGUAGE_CODE_MAP.get(source_lang, "auto")
        target_code = BAIDU_LANGUAGE_CODE_MAP.get(target_lang, "en")
        try:
            translation = await self._call_baidu(source_text, source_code, target_code)
        except Exception as exc:
            raise TranslationError("百度翻译失败", original_exception=exc) from exc

        duration = time.perf_counter() - start
        add_log(logs, f"Translation completed in {duration:.2f}s. Output text length: {len(translation)}.")
        return translation, duration

    async def _call_baidu(self, text: str, from_lang: str, to_lang: str) -> str:
        salt = str(random.randint(32768, 65536))
        sign_str = settings.baidu_translate_app_id + text + salt + settings.baidu_translate_secret_key
        sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

        params = {
            "q": text,
            "from": from_lang,
            "to": to_lang,
            "appid": settings.baidu_translate_app_id,
            "salt": salt,
            "sign": sign,
        }
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                result = await response.json()

        if "error_code" in result:
            raise RuntimeError(f"百度翻译API错误: {result.get('error_msg', '未知错误')}")
        if "trans_result" not in result:
            raise RuntimeError("翻译结果格式错误")

        return "\n".join(item["dst"] for item in result["trans_result"])
