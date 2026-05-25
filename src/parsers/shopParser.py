from defusedxml import ElementTree as ET
from utils.validators import is_item_type_valid, is_positive_int


DEFAULT_DESCRIPTION = "Description inconnue"
DEFAULT_ITEM_NAME = "Nom d'objet inconnu"


class ShopParser:
    """Parse shop XML rewards into item dictionaries."""

    def __init__(self, xml_path):
        """Load XML content immediately."""
        self.xml_path = xml_path
        self.data = self._load()

    def _load(self):
        """Return parsed item dictionaries."""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        items = []

        if not root:
            return items

        for item in root.findall("objet"):
            item_id_str = (item.get("id") or "").strip()
            item_name_str = (item.findtext("nom") or DEFAULT_ITEM_NAME).strip()
            item_type_str = (item.findtext("type") or "").strip()
            item_price_str = (item.findtext("prix") or "").strip()
            item_description_str = (
                item.findtext("description") or DEFAULT_DESCRIPTION
            ).strip()

            if False in (
                is_item_type_valid(item_type_str),
                is_positive_int(item_id_str),
                is_positive_int(item_price_str),
            ):
                continue
            items.append(
                {
                    "id_item": int(item_id_str),
                    "name": item_name_str,
                    "item_type": item_type_str,
                    "description": item_description_str,
                    "price_points": int(item_price_str),
                }
            )

        return items

    def get_items(self):
        """Return loaded item dictionaries."""
        return self.data
