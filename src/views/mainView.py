from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
)

from views.usersView import UsersView
from views.coursesView import CoursesView
from views.summariesView import SummariesView
from session import Session


class HomePage(QWidget):
    def __init__(self, parent_main):
        super().__init__()
        layout = QVBoxLayout(self)

        btn_users = QPushButton("Compte")
        btn_courses = QPushButton("Cours")
        btn_summaries = QPushButton("Résumés")
        btn_logout = QPushButton("Se déconnecter")

        btn_users.clicked.connect(parent_main.open_users)
        btn_courses.clicked.connect(parent_main.open_courses)
        btn_summaries.clicked.connect(parent_main.open_summaries)
        btn_logout.clicked.connect(parent_main.logout)

        layout.addWidget(btn_users)
        layout.addWidget(btn_courses)
        layout.addWidget(btn_summaries)
        layout.addWidget(btn_logout)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plateforme de résumés")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self)
        self.users_page = UsersView(self)
        self.courses_page = CoursesView(self)
        self.summaries_page = SummariesView(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.users_page)
        self.stack.addWidget(self.courses_page)
        self.stack.addWidget(self.summaries_page)

        self.stack.setCurrentWidget(self.home_page)

    def open_users(self):
        self.stack.setCurrentWidget(self.users_page)

    def open_courses(self):
        self.stack.setCurrentWidget(self.courses_page)

    def open_summaries(self):
        self.stack.setCurrentWidget(self.summaries_page)

    def go_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def logout(self):
        from views.connectionView import ConnectionView

        Session.logout()
        self.connection = ConnectionView()
        self.connection.show()
        self.close()
