from repositories.pointsRepository import PointsRepository
from repositories.shopRepository import ShopRepository
from repositories.usersRepository import UsersRepository
from session import Session


class ShopService:
    """Business logic for shop actions."""

    def __init__(self):
        self.repo = ShopRepository()
        self.users_repo = UsersRepository()
        self.points_repo = PointsRepository()

    def _current_user_id(self):
        """Resolve the authenticated user id from session."""
        if not Session.is_authenticated():
            return None

        user = self.users_repo.find_by_username(Session.user)
        if not user:
            return None

        return user[0]

    def list_items(self):
        """Return all available shop items."""
        return self.repo.get_all_items()

    def list_inventory(self):
        """Return the authenticated user's inventory."""
        user_id = self._current_user_id()
        if user_id is None:
            return None
        return self.repo.get_user_inventory(user_id)

    def buy_item(self, item_id):
        """Purchase one item for the authenticated user."""
        user_id = self._current_user_id()
        if user_id is None:
            return False
        return self.repo.purchase_item(user_id, item_id, self.points_repo)

    def activate_item(self, item_id):
        """Activate one owned item for the authenticated user."""
        user_id = self._current_user_id()
        if user_id is None:
            return False
        return self.repo.activate_item(user_id, item_id)

    def get_active_item(self, item_type):
        """Return active item by type for the authenticated user."""
        user_id = self._current_user_id()
        if user_id is None:
            return None
        return self.repo.get_active_item(user_id, item_type)
    
    def request6(self):
        req_6 = self.repo.additional_request_6()
        return req_6
