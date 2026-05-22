from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QDialog,
    QTextEdit,
)

from services.coursesService import CoursesService
from session import Session


class CoursesView(QWidget):
    """Courses page to list and create courses."""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.service = CoursesService()
        self.setWindowTitle("Cours")
        self.setMinimumSize(800, 600)
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_list = QPushButton("Voir la liste des cours")
        self.btn_add = QPushButton("Ajouter un cours")
        self.btn_back = QPushButton("Retour")
        self.btn_list.clicked.connect(self.view_list)
        self.btn_add.clicked.connect(self.view_add)
        self.btn_back.clicked.connect(self.main_window.go_home)
        layout.addWidget(self.btn_list)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

    def view_list(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return

        courses = self.service.list_courses()
        if not courses:
            QMessageBox.information(self, "Cours", "Aucun cours disponible.")
            return

        text = "\n".join(f"{c[0]} | {c[1]} | {c[2]} | {c[3]}" for c in courses)

        dialog = QDialog(self)
        dialog.setWindowTitle("Liste des cours")
        dialog.resize(700, 500)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.accept)

        layout.addWidget(text_edit)
        layout.addWidget(close_btn)

        dialog.exec()

    def view_add(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        code, ok1 = QInputDialog.getText(self, "Code", "Code du cours:")
        if not ok1:
            return
        name, ok2 = QInputDialog.getText(self, "Nom", "Nom du cours:")
        if not ok2:
            return
        faculty, ok3 = QInputDialog.getText(self, "Faculté", "Faculté:")
        if not ok3:
            return
        academic_year, ok4 = QInputDialog.getText(
            self, "Année académique", "Année académique (ex: 2025-2026):"
        )
        if not ok4:
            return
        inserted = self.service.add_course(
            code.strip(), name.strip(), faculty.strip(), academic_year.strip()
        )
        if inserted:
            QMessageBox.information(self, "OK", "Cours ajouté")
        else:
            QMessageBox.warning(
                self, "Erreur", "Cours déjà existant ou données invalides"
            )
