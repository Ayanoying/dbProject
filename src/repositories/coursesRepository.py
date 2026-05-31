from dbConnection import get_connection


class CoursesRepository:
    """Data access for courses."""

    def save_many(self, courses):
        """Insert multiple courses from parsed data."""
        connection = get_connection()
        cursor = connection.cursor()

        # Default academic year inserted because not provided
        cursor.execute(
            """
            INSERT INTO academic_years (id_academic_year)
            VALUES ('2025-2026')
            ON CONFLICT DO NOTHING;
            """
        )

        for course in courses:
            cursor.execute(
                """
                INSERT INTO courses (course_code, course_title, faculty, credits, academic_year_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (course_code) DO NOTHING;
                """,
                (
                    course["course_code"],
                    course["course_title"],
                    course["faculty"],
                    course.get("credits", 5),
                    course["academic_year_id"],
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(self):
        """Return all courses sorted by ID."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_course, course_code, course_title, faculty, credits, academic_year_id
            FROM courses
            ORDER BY id_course;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def add_course(
        self, course_code, course_title, faculty, academic_year_id, credits=5
    ):
        """Insert one course and return True if inserted."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO courses (course_code, course_title, faculty, credits, academic_year_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (course_code) DO NOTHING
            RETURNING id_course;
            """,
            (
                course_code.strip(),
                course_title.strip(),
                faculty,
                credits,
                academic_year_id,
            ),
        )

        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None

    def additional_request_3(self):
        """Return course with most summaries"""
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
        course = cursor.fetchall()
        cursor.close()
        connection.close()
        return course
