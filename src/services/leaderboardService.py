from repositories.leaderboardRepository import LeaderboardRepository


class LeaderboardService:
    """Business logic for leaderboard display"""

    def __init__(self):
        self.repo = LeaderboardRepository()

    def get_top_users(self, limit=10):
        """Return the top users sorted by points for display"""
        return self.repo.get_top_users_by_points(limit)
