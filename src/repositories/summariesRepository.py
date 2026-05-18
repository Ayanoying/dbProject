from dbConnection import get_connection

#fait le ien entre Python et la tables résumés de PostgreSQL  

class SummariesRepository:

    def save_many(self, summaries):
        conn = get_connection()
        cur = conn.cursor()

        for s in summaries:
            cur.execute("""
                SELECT id_utilisateur
                FROM utilisateurs
                WHERE nom_utilisateur = %s;
            """, (s["auteur"],))
            user_row = cur.fetchone()

            if user_row is None:
                continue
            cur.execute("""
                SELECT 1
                FROM courses
                WHERE code_cours = %s;
            """, (s["cours"],))
            course_exists = cur.fetchone()

            if course_exists is None:
                print(f"Cours inexistant ignoré : {s['cours']} pour le résumé '{s['titre']}'")
                continue

            cur.execute("""
                INSERT INTO resumes (titre, date_publication, note_moyenne, id_utilisateur, code_cours)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_utilisateur, code_cours, titre) DO NOTHING 
                """, ( # ON CONFLICT DO NOTHING pour ne pas ajoute rles doublons
                s["titre"],
                s["date_publication"],
                s["note_moyenne"],
                user_row[0],
                s["cours"]
            ))

        conn.commit()
        cur.close()
        conn.close()

    def publish(self, title, description, user_id, course_code): # Insère un nouveau résumé.
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resumes (titre, description, id_utilisateur, code_cours)
            VALUES (%s, %s, %s, %s)
            RETURNING id_resume;
        """, (title, description, user_id, course_code))
        # Returning id_resumes : PostgreSQL retourne l'ID généré automatiquement pour qu'on puisse le communiquer à l'utilisateur
        summary_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return summary_id

    def get_by_course(self, course_code): # récupère tous les résumés visibles d'un cours 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.id_resume, r.titre, r.description, r.date_publication,r.version, r.note_moyenne, u.nom_utilisateur
            FROM resumes r
            JOIN utilisateurs u ON r.id_utilisateur = u.id_utilisateur
            WHERE r.code_cours = %s AND r.visibilite = TRUE
            ORDER BY r.date_publication DESC; """, 
            (course_code,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_by_user(self, user_id): #Liste tous les résumés d'un utilisateur précis
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_resume, titre, code_cours, date_publication, version, note_moyenne
            FROM resumes
            WHERE id_utilisateur = %s
            ORDER BY date_publication DESC;
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def update(self, summary_id, title, description, user_id): # Modifie le titre/description ET incrémente automatiquement version
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE resumes
            SET titre = %s, description = %s, version = version + 1
            WHERE id_resume = %s AND id_utilisateur = %s
            RETURNING id_resume;
        """, (title, description, summary_id, user_id)) # condition : "AND id_utilisateur = %s garentit qu'on ne peut modifier que ses propres résmués "
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result is not None

    def delete(self, summary_id, user_id): # Supprime le résumé uniquement si c'est bien le bon auteur
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM resumes
            WHERE id_resume = %s AND id_utilisateur = %s
            RETURNING id_resume;""", 
            (summary_id, user_id)) # RETURNING id_resume permet de savoir si la suppression a eu lieu
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result is not None
