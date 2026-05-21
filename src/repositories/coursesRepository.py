from dbConnection import get_connection

# Fait le lien entre Python et la table courses de PostgreSQL


class CoursesRepository:
    def save_many(
        self, courses
    ):  # recoit une liste de cours et les insère dans la table
        connection = get_connection()
        cursor = connection.cursor()
        for c in courses:
            cursor.execute(
                """
                INSERT INTO courses (code_cours, nom, faculte, credits)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code_cours) DO NOTHING; """,
                (c["code_cours"], c["nom"], c["faculte"], c["credits"]),
            )
            # ON CONFLIT DO NOTHING : si le code cours existe deja, on ignore sans planter

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(
        self,
    ):  # retourne tous les cours de la bases trié par code & retourne liste de tuples
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT code_cours, nom, faculte, credits
            FROM courses
            ORDER BY code_cours;
        """)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows  # liste de tuples (code_cours, nom, faculte, credits)

    def add_course(
        self, code_cours, nom, faculte, credits
    ):  # insère un seul cours et retourne True si il est inséré & False si le code existe deja
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO courses (code_cours, nom, faculte, credits)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code_cours) DO NOTHING
            RETURNING code_cours;""",
            (code_cours, nom, faculte, credits),
        )  # RETURNING code_cours permet de voir si l'insert = réussi

        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None  # True si inséré, False si code_cours déjà existant
