from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QTextEdit,
    QMessageBox,
)

from services.specialQueriesService import SpecialQueriesService


class SpecialQueriesView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.service = SpecialQueriesService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(self.service.get_available_queries().keys())

        self.btn_run = QPushButton("Exécuter la requête")
        self.btn_back = QPushButton("Retour")

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        self.btn_run.clicked.connect(self.run_query)
        self.btn_back.clicked.connect(self.main_window.go_home)

        layout.addWidget(self.combo)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.result_area)
        layout.addWidget(self.btn_back)

    def run_query(self):
        query_name = self.combo.currentText()
        queries = self.service.get_available_queries()
        query_method_name = queries[query_name]

        try:
            headers, rows = self.service.execute_query(query_method_name)

            if not rows:
                self.result_area.setPlainText("Aucun résultat.")
            else:
                lines = [" | ".join(headers)]
                for row in rows:
                    lines.append(" | ".join(str(value) for value in row))
                self.result_area.setPlainText("\n".join(lines))

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
