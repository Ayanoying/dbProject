from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QMainWindow
)

from services.usersService import UsersService
from views.mainView import MainView
from loaders.dataLoader import load_data
from session import Session


class ConnectionView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.service = UsersService()
        self.setWindowTitle("Plateforme de résumés")
        self.setMinimumSize(800, 600)
        self.mode = None
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.layout = QVBoxLayout()
        self.btn_signup_mode = QPushButton("Inscription")
        self.btn_login_mode = QPushButton("Connexion")
        self.btn_load = QPushButton("Charger les données")
        self.btn_exit = QPushButton("Quitter")
        self.btn_signup_mode.clicked.connect(self.show_signup)
        self.btn_login_mode.clicked.connect(self.show_login)
        self.btn_load.clicked.connect(self.load_data_action)
        self.btn_exit.clicked.connect(self.close)
        self.layout.addWidget(self.btn_signup_mode)
        self.layout.addWidget(self.btn_login_mode)
        self.layout.addWidget(self.btn_load)
        self.layout.addWidget(self.btn_exit)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom d'utilisateur")
        self.name_input.hide()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.hide()
        self.action_btn = QPushButton("Valider")
        self.action_btn.hide()
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.action_btn)
        central.setLayout(self.layout)
        self.setCentralWidget(central)

    def show_signup(self):
        self.mode = "signup"
        self._prepare_form()
        self.email_input.show()
        self.action_btn.setText("S'inscrire")
        self.action_btn.clicked.connect(self.signup)

    def show_login(self):
        self.mode = "login"
        self._prepare_form()
        self.email_input.hide()
        self.action_btn.setText("Se connecter")
        self.action_btn.clicked.connect(self.login)

    def _prepare_form(self):
        self.name_input.show()
        self.action_btn.show()
        self.btn_signup_mode.hide()
        self.btn_login_mode.hide()
        self.btn_load.hide()
        self.btn_exit.hide()

    def signup(self):
        user_id = self.service.signup(
            self.name_input.text(),
            self.email_input.text()
        )
        if not user_id:
            QMessageBox.information(self, "OK", "Nom d'utilisateur ou email déjà pris.")
        else:
            Session.login(self.name_input.text())
            QMessageBox.information(self, "OK", f"Inscription réussie ! Bienvenue {Session.user}")
            self.open_main()

    def login(self):
        user = self.service.login(self.name_input.text())
        if not user:
            QMessageBox.information(self, "OK", "Utilisateur introuvable.")
        else:
            Session.login(self.name_input.text())
            QMessageBox.information(self, "OK", f"Connecté en tant que {Session.user}")
            self.open_main()

    def load_data_action(self):
        load_data()
        QMessageBox.information(self, "OK", "Données chargées avec succès!")

    def open_main(self):
        self.main = MainView()
        self.main.show()
        self.close()
