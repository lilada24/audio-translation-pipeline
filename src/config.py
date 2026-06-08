from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    baidu_translate_app_id: Optional[str] = None
    baidu_translate_secret_key: Optional[str] = None
    whisper_model: str = "small"
    server_port: int = 7860
    output_dir: str = "outputs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
