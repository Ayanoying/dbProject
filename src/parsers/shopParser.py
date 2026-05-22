from defusedxml import ElementTree as ET
from utils.validators import is_in_item_type_set


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

        for item in root.findall("objet"):
            item_id = item.get("id")
            name = (item.findtext("nom") or "").strip()
            item_type = (item.findtext("type") or "").strip()
            description = (item.findtext("description") or "").strip() or None
            price_text = (item.findtext("prix") or "").strip()

            if not name or not item_type or not price_text:
                continue

            items.append(
                {
                    "id_item": int(item_id) if item_id else None,
                    "name": name,
                    "item_type": item_type
                    if is_in_item_type_set(item_type)
                    else "Misc",
                    "description": description,
                    "price_points": int(price_text),
                }
            )

        return items

    def get_items(self):
        """Return loaded item dictionaries."""
        return self.data
