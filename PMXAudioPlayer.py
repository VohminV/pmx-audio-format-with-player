import sys
import pygame
import json
import base64
import io
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QFileDialog, QLabel
from PyQt5.QtCore import Qt

class PMXAudioPlayer:
    def __init__(self, pmx_file=None):
        self.pmx_file = pmx_file
        self.audio_data = None
        self.is_playing = False
        
        # Инициализация Pygame для работы с аудио
        pygame.mixer.init()

    def load_audio_from_pmx(self):
        if self.pmx_file is None:
            return
        
        # Открытие PMX файла
        with open(self.pmx_file, "r") as f:
            pmx_data = json.load(f)  # Загружаем данные PMX

        # Извлекаем аудио данные, закодированные в base64
        audio_base64 = pmx_data["audio"]

        # Декодируем аудио данные из base64
        compressed_audio_data = base64.b64decode(audio_base64)

        # Загружаем аудио из декодированных данных
        self.audio_data = io.BytesIO(compressed_audio_data)
        print("Аудио успешно загружено.")

    def start_playing(self):
        if self.audio_data is None:
            raise Exception("Audio data not loaded!")

        # Сначала убедимся, что файл в формате OGG
        try:
            pygame.mixer.music.load(self.audio_data, "ogg")
            pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
            self.is_playing = True
            print("Аудио воспроизводится.")
        except Exception as e:
            print(f"Ошибка при воспроизведении аудио: {e}")

    def stop_playing(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("Аудио остановлено.")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        print(f"Громкость установлена на {volume * 100}%.")


class PMXAudioPlayerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация плеера
        self.player = PMXAudioPlayer()

        # Настройки окна
        self.setWindowTitle("PMX Audio Player")
        self.setGeometry(100, 100, 300, 200)

        # Элементы интерфейса
        self.init_ui()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Кнопка для выбора PMX файла
        self.select_button = QPushButton("Выбрать PMX файл", self)
        self.select_button.clicked.connect(self.select_pmx_file)
        layout.addWidget(self.select_button)

        # Кнопка для старта воспроизведения
        self.play_button = QPushButton("Старт", self)
        self.play_button.clicked.connect(self.start_playing)
        layout.addWidget(self.play_button)

        # Кнопка для остановки воспроизведения
        self.stop_button = QPushButton("Стоп", self)
        self.stop_button.clicked.connect(self.stop_playing)
        layout.addWidget(self.stop_button)

        # Слайдер для регулировки громкости
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Начальная громкость 50%
        self.volume_slider.valueChanged.connect(self.change_volume)
        layout.addWidget(self.volume_slider)

        # Метка для громкости
        self.volume_label = QLabel("Громкость: 50%", self)
        layout.addWidget(self.volume_label)

        # Устанавливаем layout
        self.setLayout(layout)

    def select_pmx_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Выберите PMX файл", "", "PMX Files (*.pmx);;All Files (*)", options=options)
        if file:
            self.player.pmx_file = file
            self.player.load_audio_from_pmx()
            print(f"Файл {file} выбран.")

    def start_playing(self):
        self.player.start_playing()

    def stop_playing(self):
        self.player.stop_playing()

    def change_volume(self, value):
        volume = value / 100  # Преобразуем в диапазон от 0 до 1
        self.player.set_volume(volume)
        self.volume_label.setText(f"Громкость: {value}%")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем и показываем графическое окно
    gui = PMXAudioPlayerGUI()
    gui.show()

    sys.exit(app.exec_())
