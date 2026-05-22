from dbConnection import get_connection


class PointsRepository:
    """Data access for points transactions."""

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
            INSERT INTO transactions (transaction_type, amount, user_id, summary_id, evaluation_id, item_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_transaction;
            """,
            (transaction_type, amount, user_id, summary_id, evaluation_id, item_id),
        )

        result = cursor.fetchone()

        cursor.execute(
            """
            UPDATE users
            SET profile_points = profile_points + %s
            WHERE id_user = %s;
            """,
            (amount, user_id),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return result is not None

    def get_user_histories(self, user_id):
        """Return transaction history for one user."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT transaction_type, amount, transaction_date
            FROM transactions
            WHERE user_id = %s
            ORDER BY transaction_date DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
