# This file contains all the additional queries requested by the project PDF instructions.

from dbConnection import get_connection


class SpecialQueriesRepository:
    """Data access for additional queries."""

    def get_top_users_by_points(self, limit=10):
        """Return top N users ordered by profile_points descending."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_user, username, profile_points
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
        """Return users who have summaries in at least min_courses different courses."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT u.id_user, u.username
            FROM users u
            JOIN summaries s ON u.id_user = s.user_id
            GROUP BY u.id_user, u.username
            HAVING COUNT(DISTINCT s.course_id) >= %s;
            """,
            (min_courses,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_course_with_most_summaries(self):
        """Return the course with the most summaries."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT c.id_course, c.course_title, COUNT(s.id_summary) AS nb_summaries
            FROM courses c
            JOIN summaries s ON c.id_course = s.course_id
            GROUP BY c.id_course, c.course_title
            ORDER BY nb_summaries DESC
            LIMIT 1;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_best_summary_by_course(self):
        """Return the best rated summary for each course."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT s1.id_summary, s1.title, s1.course_id, s1.average_rating
            FROM summaries s1
            WHERE s1.average_rating = (
                SELECT MAX(s2.average_rating)
                FROM summaries s2
                WHERE s2.course_id = s1.course_id
            )
            ORDER BY s1.course_id ASC;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_users_without_summaries(self):
        """Return users who have no summaries."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT u.id_user, u.username
            FROM users u
            LEFT JOIN summaries s ON u.id_user = s.user_id
            WHERE s.id_summary IS NULL;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_most_purchased_cosmetic_item(self):
        """Return the most purchased cosmetic item."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT c.id_item, c.name, COUNT(*) AS purchases_count
            FROM cosmetic_items c
            JOIN transactions t ON c.id_item = t.item_id
            WHERE t.transaction_type = 'purchase_item'
            GROUP BY c.id_item, c.name
            ORDER BY purchases_count DESC
            LIMIT 1;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_users_who_spent_more_than_have(self):
        """Return users who spent more points than they currently have."""
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
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_average_summaries_per_user(self):
        """Return the average number of summaries per user. (Includes users with 0 summaries)"""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT AVG(summary_count)
            FROM (
                SELECT u.id_user, COUNT(s.id_summary) AS summary_count
                FROM users u
                LEFT JOIN summaries s ON u.id_user = s.user_id
                GROUP BY u.id_user
            ) AS stats;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
