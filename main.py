import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
import logging
from multiprocessing import freeze_support


def setup_logging():
    """Настройка системы логирования"""
    log_dir = os.path.join(os.path.expanduser('~'), '.anonymizer', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'anonymizer.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('anonymizer')


def setup_app_paths():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(os.path.expanduser('~'), '.anonymizer')
    os.makedirs(data_dir, exist_ok=True)

    temp_dir = os.path.join(data_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    resources_dir = os.path.join(application_path, 'resources')
    os.makedirs(resources_dir, exist_ok=True)

    styles_dir = os.path.join(resources_dir, 'styles')
    os.makedirs(styles_dir, exist_ok=True)

    icons_dir = os.path.join(resources_dir, 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    return {
        'app_path': application_path,
        'data_dir': data_dir,
        'temp_dir': temp_dir,
        'resources_dir': resources_dir,
        'styles_dir': styles_dir,
        'icons_dir': icons_dir
    }


def setup_translations(app, app_paths):
    """Настройка переводов приложения"""
    translator = QTranslator()
    translations_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load(QLocale.system(), "qtbase", "_", translations_path)
    app.installTranslator(translator)

    # Загрузка пользовательских переводов, если они существуют
    app_translator = QTranslator()
    user_translations_path = os.path.join(app_paths['app_path'], 'translations')
    os.makedirs(user_translations_path, exist_ok=True)
    app_translator.load(QLocale.system(), "anonymizer", "_", user_translations_path)
    app.installTranslator(app_translator)


def setup_resources(app_paths):
    """Настройка ресурсов приложения"""
    # Создаем файл стилей, если он не существует
    qss_file_path = os.path.join(app_paths['styles_dir'], 'modern_style.qss')

    if not os.path.exists(qss_file_path):
        from resources.styles.embedded_styles import MODERN_STYLE
        with open(qss_file_path, 'w', encoding='utf-8') as f:
            f.write(MODERN_STYLE)

    # Здесь можно добавить создание базовых иконок и других ресурсов


if __name__ == "__main__":
    freeze_support()

    logger = setup_logging()
    logger.info("Запуск приложения")

    try:
        # Настраиваем пути для приложения
        app_paths = setup_app_paths()
        logger.info(f"Пути приложения: {app_paths}")

        # Инициализируем приложение
        app = QApplication(sys.argv)

        # Устанавливаем переводы
        setup_translations(app, app_paths)

        # Устанавливаем информацию о приложении
        app.setApplicationName("Anonymizer")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("YourCompany")
        app.setOrganizationDomain("yourcompany.com")

        # Настраиваем ресурсы
        setup_resources(app_paths)

        # Импортируем и создаем основное окно приложения
        from modern_ui import ModernAnonymizerApp

        # Создаем и отображаем окно
        window = ModernAnonymizerApp(app_paths)
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Критическая ошибка при запуске: {str(e)}", exc_info=True)
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)