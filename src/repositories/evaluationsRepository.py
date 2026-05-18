from dbConnection import get_connection

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
