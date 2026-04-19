from repositories.rewardsRepository import RewardsRepository


class RewardsService:
    def __init__(self):
        self.repo = RewardsRepository()