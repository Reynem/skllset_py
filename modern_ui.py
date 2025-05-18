import sys
import os
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
                             QWidget, QPlainTextEdit, QStatusBar,
                             QGroupBox, QSplitter, QFrame)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# Импортируем классы анонимизатора
from anonymizer import Anonymizer, ImageAnonymizer


class ModernAnonymizerApp(QMainWindow):
    def __init__(self, app_paths=None):
        super().__init__()

        self.app_paths = app_paths or {}
        self.anonymizer = Anonymizer()
        self.image_anonymizer = ImageAnonymizer()

        self.initUI()
        self.loadStyleSheet()

    def loadStyleSheet(self):
        """Загрузка таблицы стилей QSS"""
        style_path = os.path.join(self.app_paths.get('styles_dir', ''), 'modern_style.qss')
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as style_file:
                    self.setStyleSheet(style_file.read())
            except Exception as e:
                print(f"Ошибка при загрузке стилей: {e}")

    def initUI(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('Анонимизатор персональных данных')
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(800, 600)

        # Основной контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Верхняя секция - заголовок и описание
        header_layout = QVBoxLayout()

        app_name_label = QLabel("Анонимизатор персональных данных")
        app_name_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 5px;")

        app_description = QLabel("Инструмент для автоматического удаления персональных данных из текста и изображений")
        app_description.setStyleSheet("font-size: 12px; color: #9D9D9D; margin-bottom: 15px;")

        header_layout.addWidget(app_name_label)
        header_layout.addWidget(app_description)

        # Горизонтальный разделитель
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        h_line.setStyleSheet("background-color: #3C3C3C; margin: 10px 0;")

        # Основной сплиттер для текстовой и изображений секций
        main_splitter = QSplitter(Qt.Vertical)

        # ===== ТЕКСТОВАЯ СЕКЦИЯ =====
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)

        # Группа для текстовой анонимизации
        text_group = QGroupBox("Анонимизация текста")
        text_group_layout = QVBoxLayout()

        # Горизонтальный сплиттер для полей ввода/вывода
        text_splitter = QSplitter(Qt.Horizontal)

        # Левая панель - для ввода текста
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        input_label = QLabel("Исходный текст:")
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("Введите или вставьте текст с персональными данными...")

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        # Правая панель - для результата
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)

        output_label = QLabel("Анонимизированный текст:")
        self.output_text = QPlainTextEdit()
        self.output_text.setPlaceholderText("Здесь появится обработанный текст...")
        self.output_text.setReadOnly(True)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)

        # Добавляем панели в сплиттер
        text_splitter.addWidget(input_widget)
        text_splitter.addWidget(output_widget)
        text_splitter.setSizes([500, 500])  # Равное разделение

        # Панель с кнопками действий для текста
        text_actions = QHBoxLayout()

        anonymize_button = QPushButton("Анонимизировать текст")
        anonymize_button.clicked.connect(self.anonymize_text)

        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_text)

        copy_button = QPushButton("Копировать результат")
        copy_button.clicked.connect(self.copy_result)

        text_actions.addWidget(anonymize_button)
        text_actions.addWidget(clear_button)
        text_actions.addStretch()
        text_actions.addWidget(copy_button)

        # Собираем все элементы текстовой секции
        text_group_layout.addWidget(text_splitter)
        text_group_layout.addLayout(text_actions)
        text_group.setLayout(text_group_layout)
        text_layout.addWidget(text_group)

        # ===== СЕКЦИЯ ИЗОБРАЖЕНИЙ =====
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)

        # Группа для анонимизации изображений
        image_group = QGroupBox("Анонимизация изображений")
        image_group_layout = QVBoxLayout()

        # Инструкции и кнопка выбора изображения
        image_header = QHBoxLayout()

        image_instructions = QLabel("Загрузите изображение для обнаружения и скрытия персональных данных")
        image_instructions.setStyleSheet("color: #9D9D9D;")

        self.select_image_button = QPushButton("Выбрать изображение")
        self.select_image_button.clicked.connect(self.select_image)

        image_header.addWidget(image_instructions)
        image_header.addStretch()
        image_header.addWidget(self.select_image_button)

        # Контейнер для изображений
        image_view_layout = QHBoxLayout()

        # Оригинальное изображение
        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)

        original_title = QLabel("Оригинал")
        original_title.setAlignment(Qt.AlignCenter)

        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setMinimumSize(400, 300)
        self.original_image_label.setStyleSheet(
            "border: 1px solid #3C3C3C; border-radius: 4px; background-color: #1E1E1E;")
        self.original_image_label.setText("Оригинальное изображение будет показано здесь")

        original_layout.addWidget(original_title)
        original_layout.addWidget(self.original_image_label)

        # Обработанное изображение
        processed_container = QWidget()
        processed_layout = QVBoxLayout(processed_container)

        processed_title = QLabel("Анонимизировано")
        processed_title.setAlignment(Qt.AlignCenter)

        self.processed_image_label = QLabel()
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.setMinimumSize(400, 300)
        self.processed_image_label.setStyleSheet(
            "border: 1px solid #3C3C3C; border-radius: 4px; background-color: #1E1E1E;")
        self.processed_image_label.setText("Анонимизированное изображение будет показано здесь")

        processed_layout.addWidget(processed_title)
        processed_layout.addWidget(self.processed_image_label)

        # Добавляем контейнеры изображений в лейаут
        image_view_layout.addWidget(original_container)
        image_view_layout.addWidget(processed_container)

        # Сборка секции изображений
        image_group_layout.addLayout(image_header)
        image_group_layout.addLayout(image_view_layout)
        image_group.setLayout(image_group_layout)
        image_layout.addWidget(image_group)

        # Добавляем секции в основной сплиттер
        main_splitter.addWidget(text_widget)
        main_splitter.addWidget(image_widget)
        main_splitter.setSizes([400, 400])  # Равное разделение

        # Собираем все в основной лейаут
        main_layout.addLayout(header_layout)
        main_layout.addWidget(h_line)
        main_layout.addWidget(main_splitter)

        # Статус бар
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: #9D9D9D;")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Приложение готово к работе")

        # Финальная установка виджета
        self.setCentralWidget(main_widget)

    def anonymize_text(self):
        """Обработка текста для анонимизации"""
        input_text = self.input_text.toPlainText()
        if not input_text:
            self.status_bar.showMessage("Введите текст для анонимизации")
            return

        try:
            self.status_bar.showMessage("Обработка текста...")
            anonymized_text = self.anonymizer.anonymize_text(input_text)
            self.output_text.setPlainText(anonymized_text)
            self.status_bar.showMessage("Текст успешно анонимизирован")
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при анонимизации: {str(e)}")
            traceback.print_exc()

    def clear_text(self):
        """Очистка текстовых полей"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_bar.showMessage("Текстовые поля очищены")

    def copy_result(self):
        """Копирование результата в буфер обмена"""
        text = self.output_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_bar.showMessage("Результат скопирован в буфер обмена")
        else:
            self.status_bar.showMessage("Нет текста для копирования")

    def select_image(self):
        """Выбор изображения для анонимизации"""
        file_dialog = QFileDialog()
        file_dialog.setStyleSheet(self.styleSheet())  # Применяем тот же стиль к диалогу

        image_path, _ = file_dialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if image_path:
            try:
                # Показываем оригинальное изображение
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.original_image_label.setPixmap(scaled_pixmap)
                self.original_image_label.setAlignment(Qt.AlignCenter)

                # Запускаем обработку
                self.status_bar.showMessage("Обработка изображения... Это может занять несколько секунд")
                QApplication.processEvents()  # Обновляем интерфейс

                # Анонимизируем изображение
                anon_path = self.image_anonymizer.process_image(image_path)

                if anon_path:
                    # Показываем обработанное изображение
                    anon_pixmap = QPixmap(anon_path)
                    scaled_anon_pixmap = anon_pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.processed_image_label.setPixmap(scaled_anon_pixmap)
                    self.processed_image_label.setAlignment(Qt.AlignCenter)
                    self.status_bar.showMessage(f"Изображение успешно анонимизировано: {anon_path}")
                else:
                    self.processed_image_label.setText("Персональные данные не обнаружены или произошла ошибка")
                    self.status_bar.showMessage("Не удалось анонимизировать изображение")

            except Exception as e:
                self.processed_image_label.setText("Ошибка при обработке изображения")
                self.status_bar.showMessage(f"Ошибка: {str(e)}")
                traceback.print_exc()