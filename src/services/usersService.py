from repositories.shopRepository import ShopRepository
from repositories.usersRepository import UsersRepository
from repositories.pointsRepository import PointsRepository
from utils.validators import is_email_valid


class UsersService:
    """Business logic for user operations."""

    def __init__(self):
        self.repo = UsersRepository()
        self.points_repo = PointsRepository()
        self.shop_repo = ShopRepository()

    def signup(self, username, email):
        """Create a user account with input and constraint validation.

        Returns:
            int: newly created user id.
            str: one of `missing_fields`, `invalid_email`, `already_exists`, `db_error`.
        """
        username = (username or "").strip()
        email = (email or "").strip()

        if not username or not email:
            return "missing_fields"

        if not is_email_valid(email):
            return "invalid_email"

        existing_username = self.repo.find_by_username(username)
        if existing_username:
            return "already_exists"

        existing_email = self.repo.find_by_email(email)
        if existing_email:
            return "already_exists"

        user_id = self.repo.register(username, email)
        return user_id

    def login(self, username):
        """Return a user row for authentication."""
        user = self.repo.find_by_username(username)
        if not user:
            return None
        return user

    def see_profile(self, username):
        """Return profile data formatted for the UI."""
        user = self.repo.find_by_username(username)
        if not user:
            return None

        active_item = ""
        active_item_id = user[6]
        if active_item_id is not None:
            active_item = self.shop_repo.get_item_by_id(active_item_id)
            if active_item:
                item_name = active_item[1]
                active_item = item_name
        return {
            "username": user[1],
            "email": user[2],
            "date": user[3],
            "level": user[4],
            "points": user[5],
            "title-badge": active_item,
        }

    def see_points_history(self, username):
        """Return points transaction history for a username."""
        user = self.repo.find_by_username(username)
        if not user:
            return None
        history = self.points_repo.get_user_histories(user[0])
        return history
