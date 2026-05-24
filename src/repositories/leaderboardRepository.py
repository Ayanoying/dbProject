from dbConnection import get_connection


class LeaderboardRepository:
    """Data access for leaderboard queries """

    def get_top_users_by_points(self, limit=10):
        """Return the top N users ordered by profile_points descending """
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
        """Return users who published summaries in at least min_courses different courses """
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
        """Return users who have never published a summary (Query 5 from spec) """
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