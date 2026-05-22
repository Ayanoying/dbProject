from dbConnection import get_connection


class ShopRepository:
    """Data access for cosmetic shop operations."""

    def get_all_items(self):
        """Return all shop items ordered by ascending id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_item, name, item_type, description, price_points
            FROM cosmetic_items
            ORDER BY id_item ASC;
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def save_many(self, items):
        """Insert many catalog items from XML data."""
        connection = get_connection()
        cursor = connection.cursor()
        for it in items:
            if it.get("id_item") is not None:
                cursor.execute(
                    """
                    INSERT INTO cosmetic_items (id_item, name, item_type, description, price_points)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id_item) DO NOTHING;
                    """,
                    (
                        it.get("id_item"),
                        it.get("name"),
                        it.get("item_type"),
                        it.get("description"),
                        it.get("price_points"),
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO cosmetic_items (name, item_type, description, price_points)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING;
                    """,
                    (
                        it.get("name"),
                        it.get("item_type"),
                        it.get("description"),
                        it.get("price_points"),
                    ),
                )

        connection.commit()
        cursor.close()
        connection.close()

    def get_item_by_id(self, item_id):
        """Return one item row by id."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id_item, name, item_type, description, price_points
            FROM cosmetic_items
            WHERE id_item = %s;
            """,
            (item_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    def get_user_inventory(self, user_id):
        """Return items owned by a user and whether each one is active."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT ci.id_item,
                   ci.name,
                   ci.item_type,
                   ci.price_points,
                   (u.active_item_id = ci.id_item) AS is_active
            FROM inventory_items ii
            JOIN cosmetic_items ci ON ii.item_id = ci.id_item
            JOIN users u ON u.id_user = ii.user_id
            WHERE ii.user_id = %s
            ORDER BY ci.item_type, ci.name;
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_active_item(self, user_id, item_type):
        """Return the active item for a given type, if any."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT ci.id_item, ci.name
            FROM users u
            JOIN cosmetic_items ci ON u.active_item_id = ci.id_item
            WHERE u.id_user = %s
            AND ci.item_type = %s
            """,
            (user_id, item_type),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    def purchase_item(self, user_id, item_id, points_repo):
        """Purchase an item if the user has enough points and does not own it yet."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT price_points
            FROM cosmetic_items
            WHERE id_item = %s;
            """,
            (item_id,),
        )
        result = cursor.fetchone()
        if not result:
            cursor.close()
            connection.close()
            return False

        price = result[0]

        cursor.execute(
            """
            SELECT profile_points
            FROM users
            WHERE id_user = %s;
            """,
            (user_id,),
        )
        user_result = cursor.fetchone()
        if not user_result or user_result[0] < price:
            cursor.close()
            connection.close()
            return False

        cursor.execute(
            """
            SELECT 1 FROM inventory_items
            WHERE user_id = %s AND item_id = %s;
            """,
            (user_id, item_id),
        )
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return False

        cursor.execute(
            """
            INSERT INTO inventory_items (user_id, item_id)
            VALUES (%s, %s);
            """,
            (user_id, item_id),
        )

        points_repo.add_transaction("purchase_item", -price, user_id, item_id=item_id)

        connection.commit()
        cursor.close()
        connection.close()
        return True

    def activate_item(self, user_id, item_id):
        """Set one owned item as active for a user."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM inventory_items
            WHERE user_id = %s AND item_id = %s;
            """,
            (user_id, item_id),
        )
        if cursor.fetchone() is None:
            cursor.close()
            connection.close()
            return False

        cursor.execute(
            """
            UPDATE users
            SET active_item_id = %s
            WHERE id_user = %s;
            """,
            (item_id, user_id),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return True

    def user_owns_item(self, user_id, item_id):
        """Return whether a user owns an item."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 1 FROM inventory_items
            WHERE user_id = %s AND item_id = %s;
            """,
            (user_id, item_id),
        )
        result = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return result
