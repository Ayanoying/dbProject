from PyQt6.QtWidgets import (
    QMainWindow, QWidget, 
    QVBoxLayout, QPushButton
)

from views.usersView import UsersView
from views.coursesView import CoursesView
from views.summariesView import SummariesView


class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plateforme de résumés")
        self.setMinimumSize(800, 600)

        self.users_view = None
        self.courses_view = None
        self.summaries_view = None

        self.init_ui()

    def init_ui(self):

        central = QWidget()
        layout = QVBoxLayout()

        btn_users = QPushButton("Compte")
        btn_courses = QPushButton("Cours")
        btn_summaries = QPushButton("Résumés")
        btn_exit = QPushButton("Se déconnecter")

        btn_users.clicked.connect(self.open_users)
        btn_courses.clicked.connect(self.open_courses)
        btn_summaries.clicked.connect(self.open_summaries)
        btn_exit.clicked.connect(self.close)

        layout.addWidget(btn_users)
        layout.addWidget(btn_courses)
        layout.addWidget(btn_summaries)
        layout.addWidget(btn_exit)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def open_users(self):
        self.users_view = UsersView()
        self.users_view.show()

    def open_courses(self):
        self.courses_view = CoursesView()
        self.courses_view.show()

    def open_summaries(self):
        self.summaries_view = SummariesView()
        self.summaries_view.show()
