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

        if root is None:
            return items

        for item in root.findall("objet"):
            item_id = item.get("id")
            name = (item.findtext("nom") or "Nom inconnu").strip()
            item_type = (item.findtext("type") or "Type inconnu").strip()
            description = (
                item.findtext("description") or "Description inconnue"
            ).strip()
            price_text = (item.findtext("prix") or "Prix inconnu").strip()
            id_item = int(item_id) if item_id and item_id.isdigit() else None

            items.append(
                {
                    "id_item": id_item,
                    "name": name,
                    "item_type": item_type
                    if is_in_item_type_set(item_type)
                    else "Misc",
                    "description": description,
                    "price_points": int(price_text)
                    if price_text.isdigit()
                    else price_text,
                }
            )

        return items

    def get_items(self):
        """Return loaded item dictionaries."""
        return self.data
