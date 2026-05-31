from dbConnection import get_connection


class SummariesRepository:
    """Data access for summaries."""

    @staticmethod
    def _find_course_id(cursor, course_code):
        """Return a course id from a course code."""
        cursor.execute(
            """
            SELECT id_course
            FROM courses
            WHERE course_code = %s;
            """,
            (course_code,),
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def save_many(self, summaries):
        """Insert summaries parsed from XML data."""
        connection = get_connection()
        cursor = connection.cursor()

        for summary in summaries:
            cursor.execute(
                """
                SELECT id_user
                FROM users
                WHERE username = %s;
                """,
                (summary["author"],),
            )
            user_row = cursor.fetchone()
            if user_row is None:
                continue

            course_code = summary.get("course_code")
            course_id = self._find_course_id(cursor, course_code)
            if course_id is None:
                continue

            cursor.execute(
                """
                SELECT 1
                FROM summaries
                WHERE user_id = %s AND course_id = %s AND title = %s;
                """,
                (user_row[0], course_id, summary["title"]),
            )
            if cursor.fetchone() is not None:
                continue

            cursor.execute(
                """
                INSERT INTO summaries (title, description, publication_date, version, visible, average_rating, user_id, course_id)
                VALUES (%s, %s, COALESCE(%s, CURRENT_DATE), %s, TRUE, %s, %s, %s);
                """,
                (
                    summary["title"],
                    summary.get("description"),
                    summary["publication_date"],
                    "v1",
                    summary["average_rating"],
                    user_row[0],
                    course_id,
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def publish(self, title, description, user_id, course_code):
        """Publish a new summary for one user and one course."""
        connection = get_connection()
        cursor = connection.cursor()

        course_id = self._find_course_id(cursor, course_code)
        if course_id is None:
            cursor.close()
            connection.close()
            return None

        cursor.execute(
            """
            INSERT INTO summaries (title, description, publication_date, version, visible, average_rating, user_id, course_id)
            VALUES (%s, %s, CURRENT_DATE, %s, TRUE, NULL, %s, %s)
            RETURNING id_summary;
            """,
            (title, description, "v1", user_id, course_id),
        )

        row = cursor.fetchone()
        if row is None:
            connection.rollback()
            cursor.close()
            connection.close()
            return None

        summary_id = row[0]
        connection.commit()
        cursor.close()
        connection.close()
        return summary_id

    def get_by_id(self, summary_id):
        """Return one summary by id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_summary, title, description, user_id, course_id
            FROM summaries
            WHERE id_summary = %s;
            """,
            (summary_id,),
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def get_by_course(self, course_code):
        """Return all visible summaries for one course code."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT s.id_summary, s.title, s.description, s.publication_date, s.version, s.average_rating, u.username, c.course_code, c.course_title
            FROM summaries s
            JOIN users u ON s.user_id = u.id_user
            JOIN courses c ON s.course_id = c.id_course
            WHERE c.course_code = %s AND s.visible = TRUE
            ORDER BY s.publication_date DESC;
            """,
            (course_code,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_by_user(self, user_id):
        """Return all summaries authored by one user."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT s.id_summary, s.title, s.description, s.publication_date, s.version, s.average_rating, c.course_code, c.course_title
            FROM summaries s
            JOIN courses c ON s.course_id = c.id_course
            WHERE s.user_id = %s AND s.visible = TRUE
            ORDER BY s.publication_date DESC;
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def update(self, summary_id, title, description, user_id):
        """Update one summary when it belongs to the user."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE summaries
            SET title = %s, description = %s
            WHERE id_summary = %s AND user_id = %s
            RETURNING id_summary;
            """,
            (title, description, summary_id, user_id),
        )
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None

    def delete(self, summary_id, user_id):
        """Soft delete one summary when it belongs to the user."""
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE summaries
                SET visible = FALSE
                WHERE id_summary = %s AND user_id = %s AND visible = TRUE
                RETURNING id_summary;
                """,
                (summary_id, user_id),
            )
            result = cursor.fetchone()
            connection.commit()
            return result is not None

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def additional_request_4(self):
        """Return the best average summaries note for each course."""
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

    def additional_request_8(self):
        """Return the average number of summaries published per user."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT AVG(nb_summaries) AS average_summaries
            FROM (
                SELECT COUNT(*) AS nb_summaries
                FROM summaries
                GROUP BY user_id
            ) AS stats;
            """
        )
        number = cursor.fetchone()
        cursor.close()
        connection.close()
        return number
