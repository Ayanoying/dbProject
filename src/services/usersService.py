from repositories.usersRepository import UsersRepository  # importe le repository

class UsersService:
    def __init__(self):
        self.repo = UsersRepository()  # crée une instance du repository à utiliser

    def inscrire(self, nom_utilisateur, email):
        existing = self.repo.find_by_username(nom_utilisateur)  # vérifie si le nom existe déjà
        if existing:
            print(f"Erreur : le nom d'utilisateur '{nom_utilisateur}' est déjà pris.")
            return None  # on s'arrête <=> pas d'inscription
        user_id = self.repo.register(nom_utilisateur, email)  # sinon on insère dans la DB
        print(f"Inscription réussie ! Bienvenue {nom_utilisateur} (id: {user_id})")
        return user_id

    def connecter(self, nom_utilisateur):
        user = self.repo.find_by_username(nom_utilisateur)  # cherche le user dans la DB
        if not user:
            print(f"Utilisateur '{nom_utilisateur}' introuvable.")
            return None
        print(f"Connecté en tant que {user[1]}")  # user[1] = nom_utilisateur
        return user  # retourne toutes les infos du user connecté

    def voir_profil(self, nom_utilisateur):  
        user = self.repo.find_by_username(nom_utilisateur)
        if not user:
            print("Utilisateur introuvable.")
            return
        print(f"""
        --- Profil de {user[1]} ---
        Email        : {user[2]}
        Inscription  : {user[3]}
        Niveau       : {user[4]}    
        Points       : {user[5]} """) # 
        
        # user[1] = nom_utilisateur
        # user[2] = email
        # user[3] = date_inscription
        # user[4] = niveau
        # user[5] = nombre_points 

    def voir_profil(self, nom_utilisateur):
        user = self.repo.find_by_username(nom_utilisateur)
        if not user:
            print("Utilisateur introuvable.")
            return
        print(f"""
            Profil de {user[1]}   user[1] = nom_utilisateur
            Email        : {user[2]}      # user[2] = email
            Inscription  : {user[3]}      # user[3] = date_inscription
            Niveau       : {user[4]}      # user[4] = niveau
            Points       : {user[5]}      # user[5] = nombre_points """)

# contient la logique métier, vérifie les règles 