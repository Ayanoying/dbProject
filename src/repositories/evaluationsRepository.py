from dbConnection import get_connection
import psycopg2

class EvaluationsRepository:
    def save_many(self, evaluations):
        conn = get_connection()
        cur = conn.cursor()
        for e in evaluations:
            cur.execute("""
                SELECT id_resume FROM resumes
                WHERE code_cours = %s AND titre = %s
                LIMIT 1;
            """, (e["resume"]["cours"], e["resume"]["titre"]))
            row = cur.fetchone()
            if row is None:
                continue

            summary_id = row[0]

            cur.execute("""
                SELECT id_utilisateur FROM utilisateurs
                WHERE nom_utilisateur = %s;
            """, (e["auteur"],))
            author_row = cur.fetchone()
            if author_row is None:
                continue

            cur.execute("""
                INSERT INTO evaluations (note, commentaire, id_auteur, id_resume)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_auteur, id_resume) DO NOTHING;
            """, (e["note"], e["commentaire"], author_row[0], summary_id))

        conn.commit()
        cur.close()
        conn.close()
    
    def add_evaluation(self, note, commentaire, id_auteur, id_resume):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO evaluations (note, commentaire, id_auteur, id_resume)
                VALUES (%s, %s, %s, %s)
                RETURNING id_evaluation;
            """, (note, commentaire, id_auteur, id_resume))

            result = cur.fetchone()
            conn.commit()
            return result[0] if result else None
        
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return -1

        except Exception:
            conn.rollback()
            raise

        finally:
            cur.close()
            conn.close()

    def update_summary_average(self, id_resume):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE resumes
                SET note_moyenne = (
                    SELECT COALESCE(AVG(note), 0)
                    FROM evaluations
                    WHERE id_resume = %s
                )
                WHERE id_resume = %s
            """, (id_resume, id_resume))

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            cur.close()
            conn.close()
