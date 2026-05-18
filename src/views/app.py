import sys
from PyQt6.QtWidgets import QApplication
from views.connectionView import ConnectionView


class App:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = ConnectionView()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
        

def launch_app():
    app = App()
    app.run()
