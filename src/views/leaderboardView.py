from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QTabWidget,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from services.leaderboardService import LeaderboardService


class LeaderboardView(QWidget):
    """View for displaying the user leaderboard and related queries """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = LeaderboardService()
        self._build_ui()

    def _build_ui(self):
        """Construct all UI elements for the leaderboard screen """
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title 
        title = QLabel("Classement")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tabs for the 3 leaderboard views 
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1 => Top 10 users by points
        self.top_users_tab = self._build_top_users_tab()
        self.tabs.addTab(self.top_users_tab, "Top 10 Utilisateurs")

        # Tab 2 => Active contributors (>= 3 courses)
        self.contributors_tab = self._build_contributors_tab()
        self.tabs.addTab(self.contributors_tab, "Contributeurs Actifs")

        # Tab 3 => Users with no summaries
        self.inactive_tab = self._build_inactive_tab()
        self.tabs.addTab(self.inactive_tab, "Utilisateurs sans Résumé")

        # Tab 4 => Users who have spent more points than they currently have
        self.spenders_tab = self._build_spenders_tab()
        self.tabs.addTab(self.spenders_tab, "Utilisateurs Dépensiers")

        # Refresh button 
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Actualiser")
        refresh_btn.setFixedWidth(150)
        refresh_btn.clicked.connect(self.refresh)  # Reload all tables on click
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        layout.addLayout(btn_layout)

        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("Retour")
        back_btn.setFixedWidth(150)
        back_btn.clicked.connect(self.parent().go_home)
        back_layout.addStretch()
        back_layout.addWidget(back_btn)
        layout.addLayout(back_layout)

        # Load data on construction
        self.refresh()

  
    #  Tab builders                       
    def _build_top_users_tab(self):
        """Create the tab showing top 10 users by profile_points """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        description = QLabel(
            "Les 10 utilisateurs ayant le plus de points (requête 1) "
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Table: rank - username - level - points
        self.top_table = QTableWidget()
        self.top_table.setColumnCount(4)
        self.top_table.setHorizontalHeaderLabels(
            ["#", "Nom d'utilisateur", "Niveau", "Points"]
        )
        # Stretch the username column to fill available space
        self.top_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.top_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers  # Read only table
        )
        self.top_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.top_table)
        return widget

    def _build_contributors_tab(self):
        """Create the tab showing users with summaries in >= 3 courses """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        description = QLabel(
            "Utilisateurs ayant publié des résumés dans au moins 3 cours différents (requête 2)"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)

        # Table: username - number of courses
        self.contributors_table = QTableWidget()
        self.contributors_table.setColumnCount(2)
        self.contributors_table.setHorizontalHeaderLabels(
            ["Nom d'utilisateur", "Nombre de cours"]
        )
        self.contributors_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.contributors_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.contributors_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.contributors_table)
        return widget

    def _build_inactive_tab(self):
        """Create the tab showing users who never published a summary """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        description = QLabel(
            "Utilisateurs n'ayant jamais publié de résumé (requête 5) "
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Table: username - points
        self.inactive_table = QTableWidget()
        self.inactive_table.setColumnCount(2)
        self.inactive_table.setHorizontalHeaderLabels(
            ["Nom d'utilisateur", "Points"]
        )
        self.inactive_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.inactive_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.inactive_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.inactive_table)
        return widget
    
    def _build_spenders_tab(self):
        """Create the tab showing users who have spent more points than they currently have """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        description = QLabel(
            "Utilisateurs ayant dépensés plus de points que ce qu'ils n'ont actuellement (requête 7) "
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Table: username - points
        self.spenders_table = QTableWidget()
        self.spenders_table.setColumnCount(3)
        self.spenders_table.setHorizontalHeaderLabels(
            ["Nom d'utilisateur", "Points", "Points dépensés"]
        )
        self.spenders_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.spenders_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.spenders_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.spenders_table)
        return widget


    #  Data loading                                                       
    def refresh(self):
        """Reload all 3 tables from the database """
        try:
            self._load_top_users()
            self._load_contributors()
            self._load_inactive_users()
            self._load_spendings_users()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le leaderboard :\n{e}")

    def _load_top_users(self):
        """Fetch and display top 10 users by points """
        rows = self.service.get_top_users(limit=10)
        self.top_table.setRowCount(len(rows))

        for row_idx, (user_id, username, level, points) in enumerate(rows):
            rank = row_idx + 1  # 1-based ranking position

            rank_item = QTableWidgetItem(str(rank))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            username_item = QTableWidgetItem(username)
            level_item = QTableWidgetItem(str(level))
            level_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            points_item = QTableWidgetItem(str(points))
            points_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.top_table.setItem(row_idx, 0, rank_item)
            self.top_table.setItem(row_idx, 1, username_item)
            self.top_table.setItem(row_idx, 2, level_item)
            self.top_table.setItem(row_idx, 3, points_item)

    def _load_contributors(self):
        """Fetch and display active contributors (summaries in >= 3 courses) """
        rows = self.service.get_active_contributors()
        self.contributors_table.setRowCount(len(rows))

        for row_idx, (username, course_count) in enumerate(rows):
            username_item = QTableWidgetItem(username)
            count_item = QTableWidgetItem(str(course_count))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.contributors_table.setItem(row_idx, 0, username_item)
            self.contributors_table.setItem(row_idx, 1, count_item)

    def _load_inactive_users(self):
        """Fetch and display users who never published a summary """
        rows = self.service.get_inactive_users()
        self.inactive_table.setRowCount(len(rows))

        for row_idx, (user_id, username, points) in enumerate(rows):
            username_item = QTableWidgetItem(username)
            points_item = QTableWidgetItem(str(points))
            points_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.inactive_table.setItem(row_idx, 0, username_item)
            self.inactive_table.setItem(row_idx, 1, points_item)
    
    def _load_spendings_users(self):
        """Fetch and display users who have spent more points than they currently have """
        users = self.service.get_spending_users()
        self.spenders_table.setRowCount(len(users))

        for row_idx, (user_id, username, points, points_spents) in enumerate(users):
            username_item = QTableWidgetItem(username)
            points_item = QTableWidgetItem(str(points))
            points_spents_item = QTableWidgetItem(str(points_spents))
            points_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            points_spents_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.spenders_table.setItem(row_idx, 0, username_item)
            self.spenders_table.setItem(row_idx, 1, points_item)
            self.spenders_table.setItem(row_idx, 2, points_spents_item)
