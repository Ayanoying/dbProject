from dbConnection import (
    get_connection,
)  # importe la fonction qui ouvre une connexion PostgreSQL


class UsersRepository:
    def save_many(self, users):  # insère une liste d'utilisateurs (venant du XML)
        connection = get_connection()  # ouvre la connexion à la base
        cursor = connection.cursor()  # crée un curseur pour exécuter du SQL
        for u in users:  # boucle sur chaque utilisateur
            cursor.execute(
                """
                INSERT INTO utilisateurs (nom_utilisateur, email, date_inscription, niveau, nombre_points)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nom_utilisateur) DO NOTHING;
                -- si le nom existe déjà, on ne fait rien (pas d'erreur)""",
                (
                    u["nom_utilisateur"],
                    u["email"],
                    u["date_inscription"],
                    u["niveau"],
                    u["nombre_points"],
                ),
            )

        connection.commit()  # valide toutes les insertions
        cursor.close()  # ferme le curseur
        connection.close()  # ferme la connexion

    def register(self, username, email):  # inscription d'un nouveau user via l'appli
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO utilisateurs (nom_utilisateur, email)
            VALUES (%s, %s)
            RETURNING id_utilisateur;  -- PostgreSQL retourne l'id qu'il vient de générer """,
            (username, email),
        )

        user_id = cursor.fetchone()[0]  # on récupère cet id généré automatiquement
        connection.commit()
        cursor.close()
        connection.close()
        return user_id  # on le retourne pour pouvoir l'utiliser ensuite

    def find_by_username(self, username):  # cherche un utilisateur par son nom
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_utilisateur, nom_utilisateur, email, date_inscription, niveau, nombre_points
            FROM utilisateurs
            WHERE nom_utilisateur = %s;  -- filtre sur le nom exact """,
            (username,),
        )

        row = cursor.fetchone()  # récupère une seule ligne (ou None si pas trouvé)
        cursor.close()
        connection.close()
        return row  # retourne un tuple (id, nom, email, date, niveau, points) ou None

    def find_by_email(self, email):  # cherche un utilisateur par son nom
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_utilisateur, nom_utilisateur, email, date_inscription, niveau, nombre_points
            FROM utilisateurs
            WHERE email = %s;  -- filtre sur le nom exact """,
            (email,),
        )

        row = cursor.fetchone()  # récupère une seule ligne (ou None si pas trouvé)
        cursor.close()
        connection.close()
        return row  # retourne un tuple (id, nom, email, date, niveau, points) ou None


# liaison à la base de données SQL
