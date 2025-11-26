from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
)

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bypass Serial Administration")
        self.setGeometry(400, 200, 500, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter Serial:")
        layout.addWidget(self.label)

        self.serial_input = QLineEdit()
        layout.addWidget(self.serial_input)

        self.add_button = QPushButton("Add Serial")
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Serial")
        layout.addWidget(self.remove_button)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def log(self, message: str):
        self.log_area.append(message)
