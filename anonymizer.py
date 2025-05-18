import re
import sys
import os
import traceback
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
                             QWidget, QPlainTextEdit,  QStatusBar)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import easyocr
import numpy as np
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    LOC,
    ORG,
    NamesExtractor,
    Doc
)

os.environ["QT_DEBUG_PLUGINS"] = "1"


class Anonymizer:
    def __init__(self):
        # Инициализация компонентов Natasha
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()

        # Инициализация эмбеддингов и тегеров
        self.emb = NewsEmbedding()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

        # Паттерн для ИИН (12 цифр)
        self.IIN_PATTERN = re.compile(r'\b\d{12}\b')
        self.IIN_REPLACEMENT = '[ИИН]'

        # Для случаев, когда Natasha может не распознать
        self.FIO_PATTERN = re.compile(r'\b[А-ЯЁ][а-яё]+(\s+[А-ЯЁ][а-яё]+){1,2}\b')
        self.FIO_ENG_PATTERN = re.compile(r'\b[A-Z][a-z]+(\s+[A-Z][a-z]+){1,2}\b')

        # Паттерны для банковских счетов и карт
        self.BANK_ACCOUNT_PATTERN_KZ_IBAN = re.compile(r'\bKZ[A-Z0-9]{18}\b', re.IGNORECASE)
        self.BANK_CARD_PATTERN = re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')

        # Паттерн для телефонных номеров (Казахстан)
        self.PHONE_PATTERN = re.compile(r'\+?7[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')

        # Паттерн для email адресов
        self.EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

        # Паттерн для адресов
        self.ADDRESS_PATTERN = re.compile(r'\b(ул|улица|пр|проспект|д|дом|кв|квартира)\.?\s+[А-Яа-яЁё0-9\s\.\,\-\/]+\b',
                                          re.IGNORECASE)

        # Замены
        self.FIO_REPLACEMENT = '[ФИО]'
        self.BANK_ACCOUNT_REPLACEMENT = '[НОМЕР СЧЕТА/КАРТЫ]'
        self.PHONE_REPLACEMENT = '[ТЕЛЕФОН]'
        self.EMAIL_REPLACEMENT = '[EMAIL]'
        self.ADDRESS_REPLACEMENT = '[АДРЕС]'
        self.ORG_REPLACEMENT = '[ОРГАНИЗАЦИЯ]'
        self.LOC_REPLACEMENT = '[МЕСТО]'

    def anonymize_text(self, input_text):
        if not input_text:
            return ""

        # Обработка паттернами для отдельных строк
        lines = input_text.split('\n')
        anonymized_lines = [self.anonymize_line(line) for line in lines]
        preprocessed_text = '\n'.join(anonymized_lines)

        # Обработка текста с помощью Natasha для лучшего распознавания сущностей
        doc = Doc(preprocessed_text)
        doc.segment(self.segmenter)
        doc.tag_ner(self.ner_tagger)

        # Замена найденных именованных сущностей
        anonymized_text = preprocessed_text

        spans = []
        for span in doc.spans:
            if span.type == PER:  # Персоны (ФИО)
                spans.append((span.start, span.stop, self.FIO_REPLACEMENT))
            elif span.type == ORG:  # Организации
                spans.append((span.start, span.stop, self.ORG_REPLACEMENT))
            elif span.type == LOC:  # Локации
                spans.append((span.start, span.stop, self.LOC_REPLACEMENT))

        # Сортируем span'ы в обратном порядке, чтобы не сбивать индексы при замене
        spans.sort(key=lambda x: x[0], reverse=True)

        # Применяем замены
        result = anonymized_text
        for start, stop, replacement in spans:
            result = result[:start] + replacement + result[stop:]

        return result

    def contains_personal_data(self, text):
        if not text:
            return False

        # Проверяем паттернами
        if (self.FIO_PATTERN.search(text) or
                self.FIO_ENG_PATTERN.search(text) or
                self.IIN_PATTERN.search(text) or
                self.BANK_ACCOUNT_PATTERN_KZ_IBAN.search(text) or
                self.BANK_CARD_PATTERN.search(text) or
                self.PHONE_PATTERN.search(text) or
                self.EMAIL_PATTERN.search(text) or
                self.ADDRESS_PATTERN.search(text)):
            return True

        # Проверяем с помощью Natasha
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_ner(self.ner_tagger)

        # Если найдена хотя бы одна сущность PER, LOC или ORG
        for span in doc.spans:
            if span.type in (PER, LOC, ORG):
                return True

        return False

    def anonymize_line(self, line):
        """Обработка строки с помощью регулярных выражений"""
        result = line

        # Обработка ИИН
        result = self.IIN_PATTERN.sub(self.IIN_REPLACEMENT, result)

        # Обработка русскоязычных ФИО через регулярные выражения (базовый уровень)
        result = self.FIO_PATTERN.sub(self.FIO_REPLACEMENT, result)

        # Обработка англоязычных ФИО
        result = self.FIO_ENG_PATTERN.sub(self.FIO_REPLACEMENT, result)

        # Обработка банковских счетов
        result = self.BANK_ACCOUNT_PATTERN_KZ_IBAN.sub(self.BANK_ACCOUNT_REPLACEMENT, result)

        # Обработка номеров карт
        result = self.BANK_CARD_PATTERN.sub(self.BANK_ACCOUNT_REPLACEMENT, result)

        # Обработка телефонов
        result = self.PHONE_PATTERN.sub(self.PHONE_REPLACEMENT, result)

        # Обработка email
        result = self.EMAIL_PATTERN.sub(self.EMAIL_REPLACEMENT, result)

        # Обработка адресов
        result = self.ADDRESS_PATTERN.sub(self.ADDRESS_REPLACEMENT, result)

        return result


class ImageAnonymizer:
    def __init__(self):
        # Инициализация модели OCR один раз при создании класса
        self.reader = easyocr.Reader(['ru', 'en'])  # Поддержка русского и английского
        self.anonymizer = Anonymizer()  # Переиспользуем текстовый анонимизатор

    def process_image(self, image_path):
        try:
            # Загрузка изображения
            image = Image.open(image_path)
            image_np = np.array(image)

            # Распознавание текста на изображении
            results = self.reader.readtext(image_np)

            # Если текст найден, обрабатываем его
            if results:
                # Создаем объект для рисования на изображении
                draw = ImageDraw.Draw(image)

                for (bbox, text, prob) in results:
                    # Проверяем, содержит ли текст персональные данные
                    if self.anonymizer.contains_personal_data(text):
                        # Координаты рамки текста
                        (top_left, top_right, bottom_right, bottom_left) = bbox

                        # Рисуем закрашенный прямоугольник поверх персональных данных
                        draw.rectangle([
                            (int(top_left[0]), int(top_left[1])),
                            (int(bottom_right[0]), int(bottom_right[1]))
                        ], fill="black")

                # Сохраняем анонимизированное изображение с префиксом 'anon_'
                base_name = os.path.basename(image_path)
                dir_path = os.path.dirname(image_path)
                anon_path = os.path.join(dir_path, f"anon_{base_name}")
                image.save(anon_path)

                return anon_path

            return None  # Если текст не найден

        except Exception as e:
            print(f"Ошибка при обработке изображения: {str(e)}")
            traceback.print_exc()
            return None


class AnonymizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.anonymizer = Anonymizer()
        self.image_anonymizer = ImageAnonymizer()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Анонимизатор персональных данных')
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет и лейаут
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Текстовые поля ввода/вывода
        input_layout = QHBoxLayout()

        # Левая панель - для текста
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Введите текст для анонимизации:"))

        self.input_text = QPlainTextEdit()
        left_panel.addWidget(self.input_text)

        text_buttons_layout = QHBoxLayout()
        anonymize_button = QPushButton("Анонимизировать текст")
        anonymize_button.clicked.connect(self.anonymize_text)

        clear_text_button = QPushButton("Очистить")
        clear_text_button.clicked.connect(self.clear_text)

        text_buttons_layout.addWidget(anonymize_button)
        text_buttons_layout.addWidget(clear_text_button)
        left_panel.addLayout(text_buttons_layout)

        # Правая панель - для результата
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Результат анонимизации:"))

        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        right_panel.addWidget(self.output_text)

        copy_button = QPushButton("Копировать результат")
        copy_button.clicked.connect(self.copy_result)
        right_panel.addWidget(copy_button)

        # Добавляем панели в основной лейаут
        input_layout.addLayout(left_panel)
        input_layout.addLayout(right_panel)
        main_layout.addLayout(input_layout)

        # Панель для изображений
        image_panel = QVBoxLayout()
        image_panel.addWidget(QLabel("Анонимизация изображений:"))

        image_buttons = QHBoxLayout()

        self.select_image_button = QPushButton("Выбрать изображение")
        self.select_image_button.clicked.connect(self.select_image)

        image_buttons.addWidget(self.select_image_button)
        image_panel.addLayout(image_buttons)

        # Добавляем контейнеры для отображения изображений
        image_view_layout = QHBoxLayout()

        self.original_image_label = QLabel("Оригинал")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setMinimumSize(300, 200)
        self.original_image_label.setStyleSheet("border: 1px solid gray")

        self.processed_image_label = QLabel("Анонимизировано")
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.setMinimumSize(300, 200)
        self.processed_image_label.setStyleSheet("border: 1px solid gray")

        image_view_layout.addWidget(self.original_image_label)
        image_view_layout.addWidget(self.processed_image_label)

        image_panel.addLayout(image_view_layout)
        main_layout.addLayout(image_panel)

        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Устанавливаем основной лейаут
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def anonymize_text(self):
        input_text = self.input_text.toPlainText()
        if not input_text:
            self.status_bar.showMessage("Введите текст для анонимизации")
            return

        try:
            anonymized_text = self.anonymizer.anonymize_text(input_text)
            self.output_text.setPlainText(anonymized_text)
            self.status_bar.showMessage("Текст успешно анонимизирован")
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при анонимизации: {str(e)}")
            traceback.print_exc()

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.status_bar.showMessage("Поля очищены")

    def copy_result(self):
        text = self.output_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_bar.showMessage("Результат скопирован в буфер обмена")

    def select_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )

        if image_path:
            try:
                # Показываем оригинальное изображение
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio)
                self.original_image_label.setPixmap(scaled_pixmap)

                # Запускаем процесс анонимизации
                self.status_bar.showMessage("Обработка изображения...")

                # Обрабатываем изображение
                anon_path = self.image_anonymizer.process_image(image_path)

                if anon_path:
                    # Показываем анонимизированное изображение
                    anon_pixmap = QPixmap(anon_path)
                    scaled_anon_pixmap = anon_pixmap.scaled(300, 200, Qt.KeepAspectRatio)
                    self.processed_image_label.setPixmap(scaled_anon_pixmap)
                    self.status_bar.showMessage(f"Изображение анонимизировано: {anon_path}")
                else:
                    self.status_bar.showMessage("Персональных данных не найдено или ошибка обработки")

            except Exception as e:
                self.status_bar.showMessage(f"Ошибка при обработке изображения: {str(e)}")
                traceback.print_exc()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = AnonymizerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        traceback.print_exc()