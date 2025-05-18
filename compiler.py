import sys
import os
from cx_Freeze import setup, Executable

packages = [
    "PyQt5", "numpy", "PIL", "easyocr", "natasha",
    "re", "traceback", "torch"
]

include_files = [
    # ("path/to/icon.ico", "icon.ico"),
    # ("path/to/assets", "assets")
    # Мне это не надо
]

# Опции для cx_Freeze
build_options = {
    "packages": packages,
    "excludes": [],
    "include_files": include_files,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "anonymizer_app.py",
        base=base,
        target_name="Anonymizer.exe",
        icon=None,
        shortcut_name="Anonymizer",
        shortcut_dir="ProgramMenuFolder"
    )
]

setup(
    name="Anonymizer",
    version="1.0.0",
    description="Приложение для анонимизации персональных данных",
    author="Your Name",
    options={"build_exe": build_options},
    executables=executables
)