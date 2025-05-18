import os
import sys
from cx_Freeze import setup, Executable

packages = [
    "PyQt5", "numpy", "PIL", "easyocr", "natasha",
    "re", "traceback", "torch", "logging", "multiprocessing"
]

include_files = [
    ("resources", "resources"),
]

excludes = [
    "tkinter", "unittest", "email", "html", "http", "urllib",
    "xml", "pydoc", "doctest", "argparse", "pdb"
]

build_options = {
    "packages": packages,
    "excludes": excludes,
    "include_files": include_files,
    "build_exe": "build/Anonymizer",
    "optimize": 2,
    "include_msvcr": True,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="Anonymizer.exe",
        icon="resources/icons/app_icon.ico",
        shortcut_name="Anonymizer",
        shortcut_dir="ProgramMenuFolder",
        copyright="Your Company © 2025",
    )
]

# Настройка установки
setup(
    name="Anonymizer",
    version="1.0.0",
    description="Приложение для анонимизации персональных данных",
    author="Your Name",
    options={"build_exe": build_options},
    executables=executables
)