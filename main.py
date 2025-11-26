import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.main_ui import MainUI
from utils import validate
from api_client import api_call

# Logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SerialApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = MainUI()
        self.connect_signals()

    def connect_signals(self):
        self.ui.add_button.clicked.connect(lambda: self.worker("register"))
        self.ui.remove_button.clicked.connect(lambda: self.worker("remove"))

    def worker(self, action: str):
        serial = self.ui.serial_input.text().strip()
        if not serial:
            QMessageBox.warning(self.ui, "Input Error", "Please enter a serial")
            return

        if not validate(serial):
            self.ui.log(f"❌ Invalid Serial: {serial}")
            return

        self.ui.log(f"📡 Sending {action} request for serial: {serial}...")

        ok, response = api_call(serial, action)

        if ok:
            self.ui.log(f"✅ Serial processed successfully: {serial}")
            self.ui.log(f"Response: {response}")
            logging.info(f"Serial processed: {serial} - Action: {action}")
        else:
            self.ui.log(f"❌ Error processing serial {serial}: {response}")
            logging.error(f"Error processing serial {serial} - Action: {action} - Response: {response}")


        self.ui.serial_input.clear()

    def run(self):
        self.ui.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = SerialApp()
    app.run()
