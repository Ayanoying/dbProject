from dbConnection import get_connection


class PointsRepository:
    def add_transaction(
        self,
        transaction_type,
        amount,
        user_id,
        summary_id=None,
        evaluation_id=None,
        item_id=None,
    ):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (type_transaction, montant, id_utilisateur, id_resume, id_evaluation, id_objet)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_transaction;""",
            (transaction_type, amount, user_id, summary_id, evaluation_id, item_id),
        )  # RETURNING id_transaction retourne l'id généré automatiquement

        result = cursor.fetchone()

        cursor.execute(
            """
            UPDATE utilisateurs
            SET nombre_points = nombre_points + %s
            WHERE id_utilisateur = %s;""",
            (amount, user_id),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return result is not None  # True si inséré, False si code_cours déjà existant

    def get_user_histories(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT type_transaction, montant, date_transaction
            FROM transactions
            WHERE id_utilisateur = %s
            ORDER BY date_transaction DESC
        """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
