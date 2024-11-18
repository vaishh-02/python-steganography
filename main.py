import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QProgressBar, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
from PIL import Image


class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography App")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel("No Image Selected", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(400)

        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Enter the secret message here...")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)

        self.embed_button = QPushButton("Embed Data", self)
        self.embed_button.setEnabled(False)
        self.embed_button.clicked.connect(self.embed_data)

        self.extract_button = QPushButton("Extract Data", self)
        self.extract_button.setEnabled(False)
        self.extract_button.clicked.connect(self.extract_data)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.select_button)
        layout.addWidget(self.embed_button)
        layout.addWidget(self.extract_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = ""
        self.output_path = "output_image.png"

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.bmp *.jpg *.jpeg)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))
            self.embed_button.setEnabled(True)
            self.extract_button.setEnabled(True)

    def embed_data(self):
        if not self.image_path:
            return

        secret_data = self.text_area.toPlainText()
        if not secret_data:
            self.text_area.setPlaceholderText("Please enter a message!")
            return

        self.progress_bar.setValue(0)
        self.animate_progress()

        QTimer.singleShot(2000, lambda: self.perform_embedding(secret_data))

    def animate_progress(self):
        self.progress_bar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 1)
        else:
            self.timer.stop()

    def perform_embedding(self, secret_data):
        image = Image.open(self.image_path)
        encoded_image = image.copy()
        width, height = image.size
        pixels = encoded_image.load()

        binary_data = ''.join(format(ord(char), '08b')
                              for char in secret_data) + '1111111111111110'
        data_index = 0

        for y in range(height):
            for x in range(width):
                if data_index < len(binary_data):
                    pixel = list(pixels[x, y])
                    for i in range(3):
                        if data_index < len(binary_data):
                            pixel[i] = pixel[i] & ~1 | int(
                                binary_data[data_index])
                            data_index += 1
                    pixels[x, y] = tuple(pixel)

        encoded_image.save(self.output_path)
        self.progress_bar.setValue(100)
        self.text_area.setText(f"Data embedded! Saved to {self.output_path}")

    def extract_data(self):
        if not self.image_path:
            return

        image = Image.open(self.image_path)
        pixels = image.load()
        width, height = image.size

        binary_data = ""
        eof_marker = '1111111111111110'

        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                for i in range(3):
                    binary_data += str(pixel[i] & 1)
                    if binary_data.endswith(eof_marker):
                        binary_data = binary_data[:-len(eof_marker)]
                        extracted_message = ''.join(
                            chr(int(binary_data[i:i + 8], 2))
                            for i in range(0, len(binary_data), 8)
                        )
                        self.text_area.setText(
                            f"Extracted Message: {extracted_message}")
                        return

        self.text_area.setText("No hidden data found.")


app = QApplication(sys.argv)
window = SteganographyApp()
window.show()
sys.exit(app.exec_())
