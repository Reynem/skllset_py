import sys
from cx_Freeze import setup, Executable

# --- Конфигурация пакетов ---
# Пакеты, которые cx_Freeze должен явно включить.
# НЕ включайте сюда модули стандартной библиотеки Python (sys, os, re, logging и т.д.)
packages = [
    "PyQt5",
    "numpy",
    "PIL",
    "easyocr",
    "natasha",
    "torch",
    # Если 'resources.styles.embedded_styles' импортируется как модуль,
    # cx_Freeze обычно находит его сам. Если нет, можно попробовать добавить:
    # "resources.styles",
]

# --- Конфигурация включаемых файлов и папок ---
# (source, destination)
# 'source' - путь к файлу/папке в вашем проекте
# 'destination' - имя файла/папки в директории сборки
include_files = [
    ("resources", "resources"), # Копирует всю папку 'resources'
    # ПРИМЕР: Если easyocr или natasha хранят модели в site-packages,
    # и их нужно скопировать (пути могут отличаться):
    # (os.path.join(sys.prefix, "Lib", "site-packages", "easyocr", "model"), "easyocr_models"),
    # (os.path.join(sys.prefix, "Lib", "site-packages", "natasha", "data"), "natasha_data"),
    # Вам нужно будет выяснить, где находятся модели и нужны ли они для копирования.
    # Альтернативно, easyocr может загружать модели при первом запуске.
]


# --- Опции сборки ---
build_options = {
    "packages": packages,
    "include_files": include_files,
    "build_exe": "build/Anonymizer",  # Папка для собранного приложения
    "optimize": 0,  # 0 для отладки, 1 или 2 для релиза
    "include_msvcr": False,  # Обычно не требуется для Python 3.5+
    # "zip_include_packages": ["*"], # Можно раскомментировать, если есть проблемы с размером/поиском
    # "zip_exclude_packages": [],
    # Иногда помогает явно указать пространства имен, если возникают проблемы с PyQt5 или другими большими пакетами
    # "namespace_packages": ["zope", "sqlalchemy"], # Пример, адаптируйте под свои нужды, если потребуется
}

# --- Определение базового исполняемого файла (для GUI на Windows) ---
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# --- Описание исполняемых файлов ---
executables = [
    Executable(
        "main.py",  # Ваш главный скрипт
        base=base,
        target_name="Anonymizer.exe",
        icon="resources/icons/icon.ico",  # Убедитесь, что путь к иконке верный
        shortcut_name="Anonymizer",
        shortcut_dir="ProgramMenuFolder",  # Ярлык в меню "Пуск"
        copyright="RizZLeris © 2025",
    )
]

# --- Настройка установки ---
setup(
    name="Anonymizer",
    version="1.0.0",
    description="Приложение для анонимизации персональных данных",
    author="RizZLeris", # Замените на ваше имя/никнейм
    options={"build_exe": build_options},
    executables=executables
)