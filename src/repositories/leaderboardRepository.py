from dbConnection import get_connection


class LeaderboardRepository:
    """Data access for leaderboard queries"""

    def get_top_users_by_points(self, limit=10):
        """Return the top N users ordered by profile_points descending"""
        connection = get_connection()
        cursor = connection.cursor()
        # Query 1 from the project spec: top users by points
        cursor.execute(
            """
            SELECT id_user, username, profile_level, profile_points
            FROM users
            ORDER BY profile_points DESC
            LIMIT %s;
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def initialize_rankings(self):
        """Initialize the rankings table based on academic years. Month or Week rankings could also be added"""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO rankings (ranking_name)
            SELECT id_academic_year
            FROM academic_years
            ON CONFLICT (ranking_name) DO NOTHING;
            """
        )

        connection.commit()
        cursor.close()
        connection.close()

    def initialize_ranking_history(self):
        """Initialize the ranking_history table with user rankings based on profile_points at a specific time."""
        connection = get_connection()
        cursor = connection.cursor()

        # Get the current ranking (could be yearly montly, weekly)
        # We couldnt get something else than yearly because no metadata about points over time were given
        cursor.execute("SELECT id_ranking FROM rankings LIMIT 1;")
        result = cursor.fetchone()

        if result:
            ranking_id = result[0]

            cursor.execute(
                """
                INSERT INTO ranking_history (user_id, ranking_id, rank, period_points)
                SELECT 
                    u.id_user,
                    %s,
                    RANK() OVER (ORDER BY u.profile_points DESC),
                    u.profile_points
                FROM users u
                ON CONFLICT (user_id, ranking_id) DO UPDATE
                SET rank = EXCLUDED.rank,
                    period_points = EXCLUDED.period_points;
                """,
                (ranking_id,),
            )

            connection.commit()

        cursor.close()
        connection.close()
