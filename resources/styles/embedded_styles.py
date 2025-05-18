# Автоматически сгенерированный модуль стилей

MODERN_STYLE = '''/* Современная тёмная тема для приложения анонимизатора */

/* Общий стиль для всего приложения */
QWidget {
    background-color: #2D2D30;
    color: #EDEDED;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Заголовок окна */
QMainWindow::title {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

/* Стиль текстовых полей */
QPlainTextEdit, QTextEdit, QLineEdit {
    background-color: #1E1E1E;
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 5px;
    color: #EDEDED;
}

QPlainTextEdit:focus, QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #007ACC;
}

/* Стиль кнопок */
QPushButton {
    background-color: #007ACC;
    border: none;
    border-radius: 4px;
    color: white;
    padding: 8px 16px;
    text-align: center;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0090EA;
}

QPushButton:pressed {
    background-color: #005A9C;
}

QPushButton:disabled {
    background-color: #3C3C3C;
    color: #9D9D9D;
}

/* Стиль меток */
QLabel {
    color: #EDEDED;
    font-weight: 500;
    padding-bottom: 5px;
}

/* Стиль панели статуса */
QStatusBar {
    background-color: #1E1E1E;
    color: #9D9D9D;
    padding: 3px;
    font-size: 9pt;
}

/* Стиль для разделителей */
QSplitter::handle {
    background-color: #3C3C3C;
}

/* Стиль для границы изображений */
QLabel[styleSheet*="border"] {
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 5px;
    background-color: #1E1E1E;
}

/* Стиль для диалогов выбора файлов */
QFileDialog {
    background-color: #2D2D30;
    color: #EDEDED;
}

/* Заголовки групп */
QGroupBox {
    border: 1px solid #3C3C3C;
    border-radius: 4px;
    padding: 10px;
    margin-top: 20px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #007ACC;
    font-weight: bold;
}

/* Стиль для полос прокрутки */
QScrollBar:vertical {
    border: none;
    background: #2D2D30;
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #5A5A5A;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #787878;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #2D2D30;
    height: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:horizontal {
    background: #5A5A5A;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #787878;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Подсветка активных элементов */
QWidget:focus {
    outline: none;
}

/* Специальный стиль для кнопки копирования */
QPushButton[text="Копировать результат"] {
    background-color: #2F8130;
}

QPushButton[text="Копировать результат"]:hover {
    background-color: #3AA03C;
}

QPushButton[text="Копировать результат"]:pressed {
    background-color: #246626;
}

/* Стиль для кнопки выбора изображения */
QPushButton[text="Выбрать изображение"] {
    background-color: #7D3C98;
}

QPushButton[text="Выбрать изображение"]:hover {
    background-color: #9B59B6;
}

QPushButton[text="Выбрать изображение"]:pressed {
    background-color: #6C3483;
}

/* Стиль для кнопки анонимизации */
QPushButton[text="Анонимизировать текст"] {
    background-color: #D35400;
}

QPushButton[text="Анонимизировать текст"]:hover {
    background-color: #E67E22;
}

QPushButton[text="Анонимизировать текст"]:pressed {
    background-color: #BA4A00;
}

/* Стиль для кнопки очистки */
QPushButton[text="Очистить"] {
    background-color: #C0392B;
}

QPushButton[text="Очистить"]:hover {
    background-color: #E74C3C;
}

QPushButton[text="Очистить"]:pressed {
    background-color: #A93226;
}'''