from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from services.leaderboardService import LeaderboardService


class LeaderboardView(QWidget):
    """View for displaying the user leaderboard and related queries"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = LeaderboardService()
        self._build_ui()

    def _build_ui(self):
        """Construct all UI elements for the leaderboard screen"""
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

        description = QLabel("Les utilisateurs ayant le plus de points")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        self.top_table = QTableWidget()
        self.top_table.setColumnCount(4)
        self.top_table.setHorizontalHeaderLabels(
            ["#", "Nom d'utilisateur", "Niveau", "Points"]
        )
        self.top_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.top_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.top_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.top_table)

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

    #  Data loading
    def refresh(self):
        """Reload the leaderboard table from the database"""
        try:
            self._load_top_users()
        except Exception as e:
            QMessageBox.critical(
                self, "Erreur", f"Impossible de charger le leaderboard :\n{e}"
            )

    def _load_top_users(self):
        """Fetch and display top 10 users by points"""
        rows = self.service.get_top_users(limit=None)
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
