from dbConnection import get_connection

# fait le ien entre Python et la tables résumés de PostgreSQL


class SummariesRepository:
    def save_many(self, summaries):
        connection = get_connection()
        cursor = connection.cursor()

        for s in summaries:
            cursor.execute(
                """
                SELECT id_utilisateur
                FROM utilisateurs
                WHERE nom_utilisateur = %s;
            """,
                (s["auteur"],),
            )
            user_row = cursor.fetchone()

            if user_row is None:
                continue
            cursor.execute(
                """
                SELECT 1
                FROM courses
                WHERE code_cours = %s;
            """,
                (s["cours"],),
            )
            course_exists = cursor.fetchone()

            if course_exists is None:
                print(
                    f"Cours inexistant ignoré : {s['cours']} pour le résumé '{s['titre']}'"
                )
                continue

            cursor.execute(
                """
                INSERT INTO resumes (titre, date_publication, note_moyenne, id_utilisateur, code_cours)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_utilisateur, code_cours, titre) DO NOTHING 
                """,
                (  # ON CONFLICT DO NOTHING pour ne pas ajoute rles doublons
                    s["titre"],
                    s["date_publication"],
                    s["note_moyenne"],
                    user_row[0],
                    s["cours"],
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def publish(
        self, title, description, user_id, course_code
    ):  # Insère un nouveau résumé.
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO resumes (titre, description, id_utilisateur, code_cours)
            VALUES (%s, %s, %s, %s)
            RETURNING id_resume;
        """,
            (title, description, user_id, course_code),
        )
        # Returning id_resumes : PostgreSQL retourne l'ID généré automatiquement pour qu'on puisse le communiquer à l'utilisateur
        summary_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        return summary_id

    def get_by_id(self, summary_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_resume, titre, description
            FROM resumes
            WHERE id_resume = %s
        """,
            (summary_id,),
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def get_by_course(
        self, course_code
    ):  # récupère tous les résumés visibles d'un cours
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT r.id_resume, r.titre, r.description, r.date_publication,r.version, r.note_moyenne, u.nom_utilisateur
            FROM resumes r
            JOIN utilisateurs u ON r.id_utilisateur = u.id_utilisateur
            WHERE r.code_cours = %s AND r.visibilite = TRUE
            ORDER BY r.date_publication DESC; """,
            (course_code,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_by_user(self, user_id):  # Liste tous les résumés d'un utilisateur précis
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_resume, titre, code_cours, date_publication, version, note_moyenne
            FROM resumes
            WHERE id_utilisateur = %s
            ORDER BY date_publication DESC;
        """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def update(
        self, summary_id, title, description, user_id
    ):  # Modifie le titre/description ET incrémente automatiquement version
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE resumes
            SET titre = %s, description = %s, version = version + 1
            WHERE id_resume = %s AND id_utilisateur = %s
            RETURNING id_resume;
        """,
            (title, description, summary_id, user_id),
        )  # condition : "AND id_utilisateur = %s garentit qu'on ne peut modifier que ses propres résmués "
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None

    def delete(
        self, summary_id, user_id
    ):  # Supprime le résumé uniquement si c'est bien le bon auteur
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM resumes
            WHERE id_resume = %s AND id_utilisateur = %s
            RETURNING id_resume;""",
            (summary_id, user_id),
        )  # RETURNING id_resume permet de savoir si la suppression a eu lieu
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None
