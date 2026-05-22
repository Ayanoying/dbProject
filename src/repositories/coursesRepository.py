from dbConnection import get_connection


class CoursesRepository:
    """Data access for courses."""

    def save_many(self, courses):
        """Insert multiple courses from parsed data."""
        connection = get_connection()
        cursor = connection.cursor()
        for course in courses:
            cursor.execute(
                """
                INSERT INTO courses (course_name, faculty, credits, academic_year_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (course_name) DO NOTHING;
                """,
                (
                    course["course_name"],
                    course["faculty"],
                    course.get("credits", 5),
                    course["academic_year_id"],
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def get_all(self):
        """Return all courses sorted by name."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_course, course_name, faculty, credits, academic_year_id
            FROM courses
            ORDER BY course_name;
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
        course_name = (
            f"{course_code.strip()} - {course_title.strip()}"
            if course_code and course_title
            else course_title.strip()
        )
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO courses (course_name, faculty, credits, academic_year_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (course_name) DO NOTHING
            RETURNING id_course;
            """,
            (course_name, faculty, credits, academic_year_id),
        )

        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result is not None
