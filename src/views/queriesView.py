from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox,
    QTextEdit, QMessageBox
)

from dbConnection import get_connection

QUERIES = {
    "1. Top 10 users with most points": """
        SELECT id_user, username, profile_points
        FROM users
        ORDER BY profile_points DESC
        LIMIT 10;
    """,
    "2. Users with summaries in at least 3 courses": """
        SELECT u.id_user, u.username
        FROM users u
        JOIN summaries s ON u.id_user = s.user_id
        GROUP BY u.id_user, u.username
        HAVING COUNT(DISTINCT s.course_id) >= 3;
    """,
    "3. Course with most summaries": """
        SELECT c.id_course, c.course_title, COUNT(s.id_summary) AS nb_summaries
        FROM courses c
        JOIN summaries s ON c.id_course = s.course_id
        GROUP BY c.id_course, c.course_title
        ORDER BY nb_summaries DESC
        LIMIT 1;
    """,
    "4. Best average summary per course": """
        SELECT s1.id_summary, s1.title, s1.course_id, s1.average_rating
        FROM summaries s1
        WHERE s1.average_rating = (
            SELECT MAX(s2.average_rating)
            FROM summaries s2
            WHERE s2.course_id = s1.course_id
        );
    """,
    "5. Users with no summary": """
        SELECT u.id_user, u.username
        FROM users u
        LEFT JOIN summaries s ON u.id_user = s.user_id
        WHERE s.id_summary IS NULL;
    """,
    "6. Most purchased cosmetic item": """
        SELECT c.id_item, c.name, COUNT(*) AS purchases_count
        FROM cosmetic_items c
        JOIN inventory_items i ON c.id_item = i.id_item
        GROUP BY c.id_item, c.name
        ORDER BY purchases_count DESC
        LIMIT 1;
    """,
    "7. Users who spent more than they currently have": """
        SELECT u.id_user, u.username, u.profile_points, SUM(ABS(t.amount)) AS total_spent
        FROM users u
        JOIN transactions t ON u.id_user = t.user_id
        WHERE t.transaction_type = 'purchase_item'
        GROUP BY u.id_user, u.username, u.profile_points
        HAVING SUM(ABS(t.amount)) > u.profile_points;
    """,
    "8. Average number of summaries per user": """
        SELECT AVG(nb_summaries) AS average_summaries
        FROM (
            SELECT COUNT(*) AS nb_summaries
            FROM summaries
            GROUP BY user_id
        ) AS stats;
    """
}

class QueriesView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(QUERIES.keys())

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
        sql = QUERIES[query_name]

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]

            if not rows:
                self.result_area.setPlainText("Aucun résultat.")
            else:
                lines = [" | ".join(headers)]
                lines.append("-" * 80)
                for row in rows:
                    lines.append(" | ".join(str(value) for value in row))
                self.result_area.setPlainText("\n".join(lines))

            cur.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Erreur SQL", str(e))