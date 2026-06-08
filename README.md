# 语音翻译流水线

这是一个本地语音翻译演示项目。它将音频文件通过以下流程转换：

1. ASR（语音识别）
2. MT（机器翻译）
3. TTS（语音合成）

## 功能

- 上传本地 `WAV` 或 `MP3` 音频
- Whisper 本地识别原文文本
- Baidu 翻译到目标语言
- Edge TTS 合成翻译后音频
- 支持指定源语言和目标语言
- 打印每个阶段耗时和日志
- 任何步骤失败时给出明确错误提示

## 依赖

已包含依赖列表：

```text
openai-whisper
edge-tts
gradio
requests
pydantic-settings
```

## 安装

推荐使用 Python 虚拟环境：

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 运行

```powershell
python app.py
```

运行后会自动打开 Gradio 页面，或者访问 `http://127.0.0.1:7860`。

## 使用说明

1. 点击上传按钮，选择一个 `WAV` 或 `MP3` 音频文件。
2. 选择源语言（可选自动检测）。
3. 选择目标语言。
4. 点击“开始翻译”。
5. 查看识别结果、翻译结果、输出音频和日志。

生成的合成音频文件会保存在 `outputs/` 目录。

## API Key 配置

该项目使用以下服务：

- Whisper：本地模型，无需 API Key
- Baidu 翻译：需要设置百度翻译 API Key
- Edge TTS：无需额外 API Key

请设置以下环境变量，或者创建项目根目录下的 `.env` 文件：

```powershell
$env:BAIDU_TRANSLATE_APP_ID="你的_app_id"
$env:BAIDU_TRANSLATE_SECRET_KEY="你的_secret_key"
$env:WHISPER_MODEL="small"
$env:SERVER_PORT=7860
```

`.env` 示例：

```text
BAIDU_TRANSLATE_APP_ID=你的_app_id
BAIDU_TRANSLATE_SECRET_KEY=你的_secret_key
WHISPER_MODEL=small
SERVER_PORT=7860
```

如果你希望改用其他商业接口，可在 `app.py` 中替换相应的 ASR、MT、TTS 调用，并说明对应环境变量配置方式。

## 项目结构说明

- `app.py`：Gradio 前端入口，负责启动服务和界面绑定
- `src/asr.py`：Whisper ASR 封装
- `src/translator.py`：百度翻译接口实现与异常封装
- `src/tts.py`：Edge TTS 合成封装
- `src/pipeline.py`：业务流程编排，使用依赖注入方式组合 ASR、翻译、TTS
- `src/config.py`：使用 `pydantic-settings` 统一读取 `.env` 和环境变量
- `src/exceptions.py`：自定义异常层次，保留原始异常链
- `src/utils.py`：公共日志与目录管理函数

注意：当前源语言/目标语言的语言代码映射为常见简写（如 `zh`、`en`、`ja` 等），其中中文映射为百度翻译支持的 `zh`。
## 注意

- 首次运行 Whisper 模型会下载模型权重，可能需要一些时间。
- 如果您在 Windows 上运行，确保已启用 `venv\Scripts\Activate.ps1`。
- 输出音频类型为 `MP3`。
