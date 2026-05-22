from utils.normalizeData import normalize_data


def is_in_faculty_set(name):
    """Return True if `name` (after normalization) is in the faculty set."""
    if not name:
        return False
    faculties_fr = {
        "informatique",
        "mathematiques",
        "sciences",
        "economie",
        "langues",
        "gestion",
    }
    return normalize_data(name) in faculties_fr


def is_in_item_type_set(name):
    """Return True if `name` (after normalization) is in the item types set."""
    if not name:
        return False
    types_fr = {"titre", "badge", "theme", "cosmetique"}
    return normalize_data(name) in types_fr
