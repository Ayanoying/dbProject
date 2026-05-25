from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QMessageBox,
    QInputDialog,
    QLineEdit,
)

from views.usersView import UsersView
from views.coursesView import CoursesView
from views.summariesView import SummariesView
from views.shopView import ShopView
from views.leaderboardView import LeaderboardView
from views.specialQueriesView import SpecialQueriesView
from session import Session


from repositories.pointsRepository import PointsRepository
from repositories.usersRepository import UsersRepository


class HomePage(QWidget):
    def __init__(self, parent_main):
        super().__init__()
        layout = QVBoxLayout(self)

        btn_users = QPushButton("Compte")
        btn_courses = QPushButton("Cours")
        btn_summaries = QPushButton("Résumés")
        btn_shop = QPushButton("Boutique")
        btn_queries = QPushButton("Centre des requêtes")
        btn_triche = QPushButton("Entrer un code de points")
        btn_leaderboard = QPushButton("Classement")
        btn_logout = QPushButton("Se déconnecter")

        btn_users.clicked.connect(parent_main.open_users)
        btn_courses.clicked.connect(parent_main.open_courses)
        btn_summaries.clicked.connect(parent_main.open_summaries)
        btn_shop.clicked.connect(parent_main.open_shop)
        btn_queries.clicked.connect(parent_main.open_queries)
        btn_triche.clicked.connect(parent_main.add_points)
        btn_leaderboard.clicked.connect(parent_main.open_leaderboard)
        btn_logout.clicked.connect(parent_main.logout)

        layout.addWidget(btn_users)
        layout.addWidget(btn_courses)
        layout.addWidget(btn_summaries)
        layout.addWidget(btn_shop)
        layout.addWidget(btn_leaderboard)
        layout.addWidget(btn_queries)
        layout.addWidget(btn_triche)
        layout.addWidget(btn_logout)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plateforme de résumés")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.points_repo = PointsRepository()
        self.users_repo = UsersRepository()

        self.home_page = HomePage(self)
        self.users_page = UsersView(self)
        self.courses_page = CoursesView(self)
        self.summaries_page = SummariesView(self)
        self.shop_page = ShopView(self)
        self.queries_page = SpecialQueriesView(self)
        self.leaderboard_page = LeaderboardView(self)

        self.stack.addWidget(self.queries_page)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.users_page)
        self.stack.addWidget(self.courses_page)
        self.stack.addWidget(self.summaries_page)
        self.stack.addWidget(self.leaderboard_page)
        self.stack.addWidget(self.shop_page)

        self.stack.setCurrentWidget(self.home_page)

    def open_users(self):
        self.stack.setCurrentWidget(self.users_page)

    def open_courses(self):
        self.stack.setCurrentWidget(self.courses_page)

    def open_summaries(self):
        self.stack.setCurrentWidget(self.summaries_page)

    def open_shop(self):
        self.stack.setCurrentWidget(self.shop_page)

    def open_leaderboard(self):
        self.stack.setCurrentWidget(self.leaderboard_page)

    def open_queries(self):
        self.stack.setCurrentWidget(self.queries_page)

    def add_points(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Pas connecté.")
            return

        code, ok = QInputDialog.getText(
            self, "Code requis", "Entrez le code secret :", QLineEdit.EchoMode.Password
        )

        if not ok:
            return

        if code not in ("joseph", "david", "cedric", "imane"):
            QMessageBox.warning(self, "Erreur", "Code incorrect.")
            return

        user = self.users_repo.find_by_username(Session.user)
        if not user:
            QMessageBox.warning(self, "Erreur", "Utilisateur introuvable.")
            return

        user_id = user[0]
        self.points_repo.add_transaction("code_points", 1000, user_id, None, None, None)

        QMessageBox.information(self, "OK", "1000 points ajoutés.")

    def go_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def logout(self):
        from views.connectionView import ConnectionView

        Session.logout()
        self.connection = ConnectionView()
        self.connection.show()
        self.close()
