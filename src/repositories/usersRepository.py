from dbConnection import get_connection


class UsersRepository:
    """Data access for users."""

    def save_many(self, users):
        """Insert multiple users from parsed data."""
        connection = get_connection()
        cursor = connection.cursor()
        for user in users:
            cursor.execute(
                """
                INSERT INTO users (username, email, registration_date, profile_level, profile_points)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (
                    user["username"],
                    user["email"],
                    user["registration_date"],
                    user["profile_level"],
                    user["profile_points"],
                ),
            )

        connection.commit()
        cursor.close()
        connection.close()

    def register(self, username, email):
        """Create a user account and return its generated id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email)
            VALUES (%s, %s)
            RETURNING id_user;
            """,
            (username, email),
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        return user_id

    def find_by_username(self, username):
        """Return one user row by username, or None."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_user, username, email, registration_date, profile_level, profile_points, active_item_id
            FROM users
            WHERE username = %s;
            """,
            (username,),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    def find_by_email(self, email):
        """Return one user row by email, or None."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_user, username, email, registration_date, profile_level, profile_points, active_item_id
            FROM users
            WHERE email = %s;
            """,
            (email,),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row
