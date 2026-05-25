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

    def get_users_with_summaries_in_multiple_courses(self, min_courses=3):
        """Return users who published summaries in at least min_courses different courses"""
        connection = get_connection()
        cursor = connection.cursor()
        # Query 2 from the project spec: users with summaries in >= 3 different courses
        cursor.execute(
            """
            SELECT u.username, COUNT(DISTINCT s.course_id) AS course_count
            FROM users u
            JOIN summaries s ON s.user_id = u.id_user
            WHERE s.visible = TRUE
            GROUP BY u.id_user, u.username
            HAVING COUNT(DISTINCT s.course_id) >= %s
            ORDER BY course_count DESC;
            """,
            (min_courses,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_users_without_summaries(self):
        """Return users who have never published a summary (Query 5 from spec)"""
        connection = get_connection()
        cursor = connection.cursor()
        # Query 5: users with no published summary at all (visible or not)
        cursor.execute(
            """
            SELECT u.id_user, u.username, u.profile_points
            FROM users u
            WHERE u.id_user NOT IN (
                SELECT DISTINCT user_id FROM summaries
            )
            ORDER BY u.username;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_users_who_spent_more_points_than_they_have(self):
        """Return users who spent more points than they currently have (Query 7)"""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT u.id_user, u.username, u.profile_points, SUM(ABS(t.amount)) AS total_spent
            FROM users u
            JOIN transactions t ON u.id_user = t.user_id
            WHERE t.transaction_type = 'purchase_item'
            GROUP BY u.id_user, u.username, u.profile_points
            HAVING SUM(ABS(t.amount)) > u.profile_points;
            """
        )
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users

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
