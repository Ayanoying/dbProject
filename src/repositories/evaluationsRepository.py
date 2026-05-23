from dbConnection import get_connection
import psycopg2


class EvaluationsRepository:
    """Data access for evaluations."""

    def save_many(self, evaluations):
        """Insert evaluation rows from parsed JSON input."""
        connection = get_connection()
        cursor = connection.cursor()
        for evaluation in evaluations:
            cursor.execute(
                """
                SELECT s.id_summary
                FROM summaries s
                JOIN courses c ON s.course_id = c.id_course
                WHERE c.course_code = %s AND s.title = %s
                LIMIT 1;
                """,
                (evaluation["resume"]["cours"], evaluation["resume"]["titre"]),
            )
            row = cursor.fetchone()
            if row is None:
                continue

            summary_id = row[0]

            cursor.execute(
                """
                SELECT id_user
                FROM users
                WHERE username = %s;
                """,
                (evaluation["auteur"],),
            )
            author_row = cursor.fetchone()
            if author_row is None:
                continue

            cursor.execute(
                """
                INSERT INTO evaluations (note, comment, user_id, summary_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, summary_id) DO NOTHING;
                """,
                (
                    evaluation["note"],
                    evaluation["commentaire"],
                    author_row[0],
                    summary_id,
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def add_evaluation(self, note, comment, user_id, summary_id):
        """Create one evaluation and return its id."""
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO evaluations (note, comment, user_id, summary_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id_evaluation;
                """,
                (note, comment, user_id, summary_id),
            )

            result = cursor.fetchone()
            connection.commit()
            return result[0] if result else None

        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            return -1

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def update_summary_average(self, summary_id):
        """Refresh derived average_rating on one summary."""
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE summaries
                SET average_rating = (
                    SELECT COALESCE(AVG(note), 0)
                    FROM evaluations
                    WHERE summary_id = %s
                )
                WHERE id_summary = %s
                """,
                (summary_id, summary_id),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()
