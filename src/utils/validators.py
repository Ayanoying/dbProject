import re

from utils.normalizeData import normalize_data


def is_faculty_valid(name_str):
    """Return True if `name` (after normalization) is in the faculty set."""
    if not name_str:
        return False
    faculties_fr = {
        "informatique",
        "mathematiques",
        "sciences",
        "economie",
        "langues",
        "gestion",
    }
    return normalize_data(name_str) in faculties_fr


def is_item_type_valid(name_str):
    """Return True if `name` (after normalization) is in the item types set."""
    if not name_str:
        return False
    types_fr = {"titre", "badge", "theme", "cosmetique"}
    return normalize_data(name_str) in types_fr


def is_course_code_valid(code_str):
    """Return True if `code` matches the course code format."""
    if not code_str:
        return False
    return re.fullmatch(r"[A-Z]{4,5}\d{3}", code_str.strip()) is not None


def is_credits_valid(credits_str):
    """Return True if `credits` is a positive integer."""
    if not credits_str:
        return False
    try:
        return 10 >= int(credits_str) > 0
    except (ValueError, TypeError):
        return False


def is_positive_int(value_str):
    """Return True if `price` is a non-negative integer."""
    if not value_str:
        return False
    try:
        return int(value_str) >= 0
    except (ValueError, TypeError):
        return False


def is_level_valid(level_str):
    """Return True if `level` is an integer between 1 and 10."""
    if not level_str:
        return False
    try:
        return int(level_str) >= 1
    except (ValueError, TypeError):
        return False


def is_average_note_valid(note_str):
    """Return True if `note` is a float between 0 and 5."""
    if not note_str:
        return False
    try:
        return 0 <= float(note_str) <= 5
    except (ValueError, TypeError):
        return False


def is_created_username_valid(username_str):
    """Return True if `username` is a non-empty string without spaces."""
    if not username_str or not isinstance(username_str, str):
        return False
    return " " not in username_str.strip()


def is_email_valid(email_str):
    """Return True if `email` is a valid email address."""
    if not email_str or not isinstance(email_str, str):
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email_str.strip()) is not None


def is_date_valid(date_str):
    """Return True if `date_str` is in YYYY-MM-DD format."""
    if not date_str or not isinstance(date_str, str):
        return False
    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(date_regex, date_str.strip()) is not None
