import os
import time


def ensure_output_dir(directory: str):
    os.makedirs(directory, exist_ok=True)


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def add_log(logs: list[str], message: str):
    logs.append(f"[{timestamp()}] {message}")
