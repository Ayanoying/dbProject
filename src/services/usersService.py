from repositories.usersRepository import UsersRepository  # importe le repository
from repositories.pointsRepository import PointsRepository


class UsersService:
    def __init__(self):
        self.repo = UsersRepository()  # crée une instance du repository à utiliser
        self.points_repo = (
            PointsRepository()
        )  # crée une instance de PointsRepository à utiliser

    def signup(self, username, email):
        existing_username = self.repo.find_by_username(
            username
        )  # vérifie si le nom existe déjà
        if existing_username:
            return None  # on s'arrête <=> pas d'inscription

        existing_email = self.repo.find_by_email(email)
        if existing_email:
            return None  # on s'arrête <=> pas d'inscription

        user_id = self.repo.register(username, email)  # sinon on insère dans la DB
        return user_id

    def login(self, username):
        user = self.repo.find_by_username(username)  # cherche le user dans la DB
        if not user:
            return None
        return user  # retourne toutes les infos du user connecté

    def see_profile(self, username):
        user = self.repo.find_by_username(username)
        if not user:
            return None
        return {
            "username": user[1],
            "email": user[2],
            "date": user[3],
            "niveau": user[4],
            "points": user[5],
        }

    def see_points_history(self, username):
        user = self.repo.find_by_username(username)
        if not user:
            return None
        history = self.points_repo.get_user_histories(user[0])
        return history


# contient la logique métier, vérifie les règles
