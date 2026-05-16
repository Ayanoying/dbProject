from repositories.usersRepository import UsersRepository  # importe le repository
from repositories.pointsRepository import PointsRepository

class UsersService:
    def __init__(self):
        self.repo = UsersRepository()  # crée une instance du repository à utiliser
        self.points_repo = PointsRepository() # crée une instance de PointsRepository à utiliser

    def inscrire(self, nom_utilisateur, email):
        existing_username = self.repo.find_by_username(nom_utilisateur)  # vérifie si le nom existe déjà
        if existing_username:
            print(f"Erreur : le nom d'utilisateur '{nom_utilisateur}' est déjà pris.")
            return None  # on s'arrête <=> pas d'inscription
        
        existing_email = self.repo.find_by_email(email)
        if existing_email:
            print(f"Erreur : l'email '{email}' est déjà utilisé.")
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
         Profil de {user[1]} :
        Email        : {user[2]}
        Inscription  : {user[3]}
        Niveau       : {user[4]}    
        Points       : {user[5]} """) # 
        
        # user[1] = nom_utilisateur
        # user[2] = email
        # user[3] = date_inscription
        # user[4] = niveau
        # user[5] = nombre_points 

    def voir_historique_points(self, nom_utilisateur):
        user = self.repo.find_by_username(nom_utilisateur)
        if not user:
            print(f"Utilisateur '{nom_utilisateur}' introuvable.")
            return

        historique = self.points_repo.get_historique_user(user[0]) #Récupère l'id utilisateur
        if not historique:
            print("Aucune transaction de points.")
            return

        print(f"\n-- Historique des transactions de {nom_utilisateur} --")
        for t in historique:
            type_transaction, montant, date_transaction = t
            signe = "+" if montant >= 0 else ""
            print(f"{date_transaction} | {type_transaction} | {signe}{montant} points")


# contient la logique métier, vérifie les règles 