from dbConnection import get_connection


class EvaluationsRepository:
    def save_many(self, evaluations):
        conn = get_connection()
        cur = conn.cursor()

        for e in evaluations:
            cur.execute("""
                INSERT INTO evaluations
                (auteur, destinataire, code_cours, titre, note, commentaire)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                e["auteur"],
                e["destinataire"],
                e["resume"]["cours"],
                e["resume"]["titre"],
                e["note"],
                e["commentaire"]
            ))

        conn.commit()
        cur.close()
        conn.close()