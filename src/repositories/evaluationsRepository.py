from dbConnection import get_connection
import psycopg2


class EvaluationsRepository:
    def save_many(self, evaluations):
        connection = get_connection()
        cursor = connection.cursor()
        for e in evaluations:
            cursor.execute(
                """
                SELECT id_resume FROM resumes
                WHERE code_cours = %s AND titre = %s
                LIMIT 1;
            """,
                (e["resume"]["cours"], e["resume"]["titre"]),
            )
            row = cursor.fetchone()
            if row is None:
                continue

            summary_id = row[0]

            cursor.execute(
                """
                SELECT id_utilisateur FROM utilisateurs
                WHERE nom_utilisateur = %s;
            """,
                (e["auteur"],),
            )
            author_row = cursor.fetchone()
            if author_row is None:
                continue

            cursor.execute(
                """
                INSERT INTO evaluations (note, commentaire, id_auteur, id_resume)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_auteur, id_resume) DO NOTHING;
            """,
                (e["note"], e["commentaire"], author_row[0], summary_id),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def add_evaluation(self, note, commentaire, id_auteur, id_resume):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO evaluations (note, commentaire, id_auteur, id_resume)
                VALUES (%s, %s, %s, %s)
                RETURNING id_evaluation;
            """,
                (note, commentaire, id_auteur, id_resume),
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

    def update_summary_average(self, id_resume):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE resumes
                SET note_moyenne = (
                    SELECT COALESCE(AVG(note), 0)
                    FROM evaluations
                    WHERE id_resume = %s
                )
                WHERE id_resume = %s
            """,
                (id_resume, id_resume),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()
