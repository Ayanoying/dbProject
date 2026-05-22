from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QInputDialog

from services.summariesService import SummariesService
from session import Session


class SummariesView(QWidget):
    """Summaries page for listing, publishing, editing, and evaluating summaries."""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.service = SummariesService()
        self.setWindowTitle("Résumés")
        self.setMinimumSize(800, 600)
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_list = QPushButton("Voir les résumés d'un cours")
        self.btn_evaluate = QPushButton("Noter un résumé")
        self.btn_list_mines = QPushButton("Voir mes résumés")
        self.btn_publish = QPushButton("Publier un résumé")
        self.btn_edit = QPushButton("Modifier un résumé")
        self.btn_delete = QPushButton("Supprimer un résumé")
        self.btn_back = QPushButton("Retour")
        self.btn_list.clicked.connect(self.view_list)
        self.btn_evaluate.clicked.connect(self.view_evaluate)
        self.btn_list_mines.clicked.connect(self.view_list_mines)
        self.btn_publish.clicked.connect(self.view_publish)
        self.btn_edit.clicked.connect(self.view_edit)
        self.btn_delete.clicked.connect(self.view_delete)
        self.btn_back.clicked.connect(self.main_window.go_home)
        layout.addWidget(self.btn_list)
        layout.addWidget(self.btn_evaluate)
        layout.addWidget(self.btn_list_mines)
        layout.addWidget(self.btn_publish)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

    def view_list(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        course_name, ok = QInputDialog.getText(self, "Cours", "Nom du cours : ")
        if not ok:
            return
        summaries = self.service.see_course_summaries(course_name.strip())
        if not summaries:
            QMessageBox.information(self, "Résumés", "Aucun résumé trouvé.")
            return
        text = ""
        for s in summaries:
            note = s[5] if s[5] is not None else "Rien"
            text += (
                f"[{s[0]}] {s[1]}\nAuteur : {s[6]}\nVersion : {s[4]}\nNote : {note}\n\n"
            )
        QMessageBox.information(self, "Résumés du cours", text)

    def view_evaluate(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return

        username = Session.user

        summary_id, ok1 = QInputDialog.getInt(self, "Résumé", "ID du résumé :")
        if not ok1:
            return

        note, ok2 = QInputDialog.getInt(self, "Note", "Note (0 à 5) :", 0, 0, 5, 1)
        if not ok2:
            return

        commentaire, ok3 = QInputDialog.getText(self, "Commentaire", "Commentaire :")
        if not ok3:
            return

        result = self.service.evaluate(username, summary_id, note, commentaire)

        if result is None:
            QMessageBox.warning(self, "Erreur", "Utilisateur introuvable.")
        elif result is False:
            QMessageBox.warning(self, "Erreur", "Résumé introuvable.")
        elif result == "invalid_note":
            QMessageBox.warning(self, "Erreur", "La note doit être entre 0 et 5.")
        elif result == "already_exists":
            QMessageBox.warning(self, "Erreur", "Vous avez déjà noté ce résumé.")
        else:
            QMessageBox.information(self, "OK", f"Évaluation ajoutée ! ID : {result}")

    def view_list_mines(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        username = Session.user
        summaries = self.service.see_my_summaries(username)
        if not summaries:
            QMessageBox.information(self, "Résumés", "Vous n'avez publié aucun résumé.")
            return
        text = ""
        for s in summaries:
            note = s[5] if s[5] is not None else "Rien"
            text += f"[{s[0]}] {s[1]}\n{s[2]}\n{s[3]}\n{s[4]} | note: {note}\n\n"
        QMessageBox.information(self, "Mes résumés", text)

    def view_publish(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        username = Session.user
        course_name, ok1 = QInputDialog.getText(self, "Cours", "Nom du cours :")
        if not ok1:
            return
        title, ok2 = QInputDialog.getText(self, "Titre", "Titre :")
        if not ok2:
            return
        desc, ok3 = QInputDialog.getText(self, "Description", "Description :")
        if not ok3:
            return
        result = self.service.publish(username, course_name.strip(), title, desc)
        if result is None:
            QMessageBox.warning(self, "Erreur", "Utilisateur introuvable.")
        elif result is False:
            QMessageBox.warning(self, "Erreur", "Cours invalide.")
        else:
            QMessageBox.information(self, "OK", f"Résumé publié ! ID : {result}")

    def view_edit(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        username = Session.user
        summary_id, ok1 = QInputDialog.getInt(self, "Modifier", "ID du résumé :")
        if not ok1:
            return
        title, ok2 = QInputDialog.getText(self, "Titre", "Nouveau titre :")
        if not ok2:
            return
        desc, ok3 = QInputDialog.getText(self, "Description", "Nouvelle description :")
        if not ok3:
            return
        ok = self.service.edit(username, summary_id, title, desc)
        if ok:
            QMessageBox.information(self, "OK", "Résumé modifié.")
        else:
            QMessageBox.warning(self, "Erreur", "Modification impossible.")

    def view_delete(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        username = Session.user
        summary_id, ok = QInputDialog.getInt(self, "Supprimer", "ID du résumé :")
        if not ok:
            return
        deleted = self.service.delete(username, summary_id)
        if deleted:
            QMessageBox.information(self, "OK", "Résumé supprimé.")
        else:
            QMessageBox.warning(self, "Erreur", "Suppression impossible.")
