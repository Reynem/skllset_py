import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
import logging
from multiprocessing import freeze_support


def setup_logging():
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

    return {
        'app_path': application_path,
        'data_dir': data_dir,
        'temp_dir': temp_dir
    }


def setup_translations(app):
    translator = QTranslator()
    translations_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load(QLocale.system(), "qtbase", "_", translations_path)
    app.installTranslator(translator)

    app_translator = QTranslator()
    app_translator.load(QLocale.system(), "anonymizer", "_", os.path.join(app_paths['app_path'], 'translations'))
    app.installTranslator(app_translator)


if __name__ == "__main__":
    freeze_support()

    logger = setup_logging()
    logger.info("Запуск приложения")

    try:
        app_paths = setup_app_paths()
        logger.info(f"Пути приложения: {app_paths}")

        app = QApplication(sys.argv)

        setup_translations(app)

        app.setApplicationName("Anonymizer")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("YourCompany")
        app.setOrganizationDomain("yourcompany.com")

        from anonymizer import AnonymizerApp

        window = AnonymizerApp()
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Критическая ошибка при запуске: {str(e)}", exc_info=True)
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)