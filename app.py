import gradio as gr

from src.config import settings
from src.pipeline import Pipeline

LANGUAGE_NAMES = {
    "auto": "Auto Detect",
    "en": "English",
    "zh": "Chinese",
    "ja": "Japanese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
}

pipeline = Pipeline()


def create_demo():
    source_choices = [
        (LANGUAGE_NAMES[key], key)
        for key in ["auto", "en", "zh", "ja", "es", "fr", "de", "it", "ko", "pt", "ru"]
    ]
    target_choices = [
        (LANGUAGE_NAMES[key], key)
        for key in ["en", "zh", "ja", "es", "fr", "de", "it", "ko", "pt", "ru"]
    ]

    with gr.Blocks(title="语音翻译流水线") as demo:
        gr.Markdown("# 语音翻译流水线\n上传 WAV 或 MP3 音频后，完成 ASR → MT → TTS 的转换。")

        with gr.Row():
            audio_input = gr.Audio(sources=["upload"], type="filepath", label="音频文件")
            with gr.Column():
                source_lang = gr.Dropdown(source_choices, value="auto", label="源语言")
                target_lang = gr.Dropdown(target_choices, value="en", label="目标语言")
                run_button = gr.Button("开始翻译")

        source_text = gr.Textbox(label="识别结果", lines=5)
        translated_text = gr.Textbox(label="翻译结果", lines=5)
        output_audio = gr.Audio(label="输出音频", type="filepath")
        log_output = gr.Textbox(label="运行日志", lines=12)

        run_button.click(
            pipeline.run,
            inputs=[audio_input, source_lang, target_lang],
            outputs=[source_text, translated_text, output_audio, log_output],
        )

        gr.Markdown(
            "---\n" 
            "支持源语言自动检测；输出音频文件保存在 `outputs/` 目录。"
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(server_name="0.0.0.0", server_port=settings.server_port)
