import sys

import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_KEY_STATIC = '8dc8f9d3-e4bc-4a5d-9333-fcce88ebc653'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.map_zoom = 10
        self.map_ll = []
        self.map_key = ''
        self.pushButton.clicked.connect(self.on_click)

    def on_click(self):
        self.map_ll = [float(i) for i in self.lineEdit.text().split()]
        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.map_zoom += 1
        if event.key() == Qt.Key.Key_PageDown:
            self.map_zoom -= 1
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "z": self.map_zoom,
            'apikey': API_KEY_STATIC}
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(' https://static-maps.yandex.ru/v1', params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.g_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
