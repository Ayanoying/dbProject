from repositories.leaderboardRepository import LeaderboardRepository


class LeaderboardService:
    """Business logic for leaderboard display """

    def __init__(self):
        self.repo = LeaderboardRepository()

    def get_top_users(self, limit=10):
        """Return the top users sorted by points for display """
        return self.repo.get_top_users_by_points(limit)

    def get_active_contributors(self):
        """Return users who published summaries in at least 3 different courses """
        return self.repo.get_users_with_summaries_in_multiple_courses(min_courses=3)

    def get_inactive_users(self):
        """Return users who never published any summary """
        return self.repo.get_users_without_summaries()

    def get_spending_users(self):
        """Return users who spent more points than they currently have """
        return self.repo.get_users_who_spent_more_points_than_they_have()