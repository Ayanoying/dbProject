from dbConnection import get_connection

# Fait le lien entre Python et la table courses de PostgreSQL


class CoursesRepository:
    def save_many(
        self, courses
    ):  # recoit une liste de cours et les insère dans la table
        conn = get_connection()
        cur = conn.cursor()
        for c in courses:
            cur.execute(
                """
                INSERT INTO courses (code_cours, nom, faculte, credits)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code_cours) DO NOTHING; """,
                (c["code_cours"], c["nom"], c["faculte"], c["credits"]),
            )
            # ON CONFLIT DO NOTHING : si le code cours existe deja, on ignore sans planter

        conn.commit()
        cur.close()
        conn.close()

    def get_all(
        self,
    ):  # retourne tous les cours de la bases trié par code & retourne liste de tuples
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT code_cours, nom, faculte, credits
            FROM courses
            ORDER BY code_cours;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows  # liste de tuples (code_cours, nom, faculte, credits)

    def add_course(
        self, code_cours, nom, faculte, credits
    ):  # insère un seul cours et retourne True si il est inséré & False si le code existe deja
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO courses (code_cours, nom, faculte, credits)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code_cours) DO NOTHING
            RETURNING code_cours;""",
            (code_cours, nom, faculte, credits),
        )  # RETURNING code_cours permet de voir si l'insert = réussi

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result is not None  # True si inséré, False si code_cours déjà existant
