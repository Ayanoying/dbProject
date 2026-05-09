from dbConnection import get_connection  # importe la fonction qui ouvre une connexion PostgreSQL

class UsersRepository:

    def save_many(self, users):      # insère une liste d'utilisateurs (venant du XML)
        conn = get_connection()       # ouvre la connexion à la base
        cur = conn.cursor()     # crée un curseur pour exécuter du SQL
        for u in users:   # boucle sur chaque utilisateur
            cur.execute("""
                INSERT INTO utilisateurs (nom_utilisateur, email, date_inscription, niveau, nombre_points)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nom_utilisateur) DO NOTHING;
                -- si le nom existe déjà, on ne fait rien (pas d'erreur)""", 
                (u["nom_utilisateur"], u["email"], u["date_inscription"], u["niveau"], u["nombre_points"]))
            
        conn.commit()   # valide toutes les insertions
        cur.close()    # ferme le curseur
        conn.close()   # ferme la connexion

    def register(self, nom_utilisateur, email):  # inscription d'un nouveau user via l'appli
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO utilisateurs (nom_utilisateur, email)
            VALUES (%s, %s)
            RETURNING id_utilisateur;  -- PostgreSQL retourne l'id qu'il vient de générer """, (nom_utilisateur, email))
        
        user_id = cur.fetchone()[0]  # on récupère cet id généré automatiquement
        conn.commit()
        cur.close()
        conn.close()
        return user_id  # on le retourne pour pouvoir l'utiliser ensuite

    def find_by_username(self, nom_utilisateur):  # cherche un utilisateur par son nom
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_utilisateur, nom_utilisateur, email, date_inscription, niveau, nombre_points
            FROM utilisateurs
            WHERE nom_utilisateur = %s;  -- filtre sur le nom exact """, (nom_utilisateur,))
        
        row = cur.fetchone()  # récupère une seule ligne (ou None si pas trouvé)
        cur.close()
        conn.close()
        return row  # retourne un tuple (id, nom, email, date, niveau, points) ou None
    
#liaison à la base de données SQL 