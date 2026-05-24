from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox

from services.usersService import UsersService
from session import Session


class UsersView(QWidget):
    """User profile and points history page """

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.service = UsersService()
        self.setWindowTitle("Compte")
        self.setMinimumSize(800, 600)
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_profile = QPushButton("Voir le profil")
        self.btn_history = QPushButton("Voir l'historique des points")
        self.btn_back = QPushButton("Retour")
        self.btn_profile.clicked.connect(self.view_profile)
        self.btn_history.clicked.connect(self.view_history)
        if self.main_window is not None:
            self.btn_back.clicked.connect(self.main_window.go_home)
        layout.addWidget(self.btn_profile)
        layout.addWidget(self.btn_history)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

    def view_profile(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        user = Session.user
        profile = self.service.see_profile(user)
        if profile is None:
            QMessageBox.warning(self, "Erreur", "Profil introuvable")
            return
        QMessageBox.information(
            self,
            "Profil",
            f"""
            Nom : {profile["username"]}
            Email : {profile["email"]}
            Inscription : {profile["date"]}
            Niveau : {profile["level"]}
            Points : {profile["points"]}
            Titre/Badge : {profile.get("title-badge")}
            """,
        )

    def view_history(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté")
            return
        user = Session.user
        history = self.service.see_points_history(user)
        if not history:
            QMessageBox.information(self, "Historique", "Aucune transaction de points.")
            return
        text = "\n".join(f"{t[2]} | {t[1]} | {t[0]}" for t in history)
        QMessageBox.information(self, "Historique des points", text)
