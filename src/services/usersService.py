from repositories.usersRepository import UsersRepository


class UsersService:
    def __init__(self):
        self.repo = UsersRepository()
