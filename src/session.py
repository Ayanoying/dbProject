class Session:
    user = None

    @classmethod
    def login(cls, user):
        cls.user = user

    @classmethod
    def logout(cls):
        cls.user = None

    @classmethod
    def is_authenticated(cls):
        return cls.user is not None
