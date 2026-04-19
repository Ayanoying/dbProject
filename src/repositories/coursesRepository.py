from dbConnection import get_connection


class CoursesRepository:
    def save_many(self, courses):
        conn = get_connection()
        cur = conn.cursor()
        for c in courses:
            cur.execute("""
                INSERT INTO courses (code_cours, nom, faculte, credits)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code_cours) DO NOTHING;
            """, (c["code_cours"], c["nom"], c["faculte"], c["credits"]))
        conn.commit()
        cur.close()
        conn.close()
