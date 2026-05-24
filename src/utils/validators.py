import re

from utils.normalizeData import normalize_data


def is_faculty_valid(name):
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


def is_item_type_valid(name):
    """Return True if `name` (after normalization) is in the item types set."""
    if not name:
        return False
    types_fr = {"titre", "badge", "theme", "cosmetique"}
    return normalize_data(name) in types_fr


def is_course_code_valid(code):
    """Return True if `code` matches the course code format."""
    if not code:
        return False
    return re.fullmatch(r"[A-Z]{4,5}\d{3}", code.strip()) is not None


def is_credits_valid(credits):
    """Return True if `credits` is a positive integer."""
    if credits is None:
        return False
    try:
        return 10 >= int(credits) > 0
    except (ValueError, TypeError):
        return False


def is_item_id_valid(item_id):
    """Return True if `item_id` is a positive integer."""
    if item_id is None:
        return False
    try:
        return int(item_id) > 0
    except (ValueError, TypeError):
        return False


def is_positive_int(value):
    """Return True if `price` is a non-negative integer."""
    if value is None:
        return False
    try:
        return int(value) >= 0
    except (ValueError, TypeError):
        return False


def is_level_valid(level):
    """Return True if `level` is an integer between 1 and 10."""
    if level is None:
        return False
    try:
        return int(level) >= 1
    except (ValueError, TypeError):
        return False


def is_average_note_valid(note):
    """Return True if `note` is a float between 0 and 5."""
    if note is None:
        return False
    try:
        return 0 <= float(note) <= 5
    except (ValueError, TypeError):
        return False


def is_created_username_valid(username):
    """Return True if `username` is a non-empty string without spaces."""
    if not username or not isinstance(username, str):
        return False
    return " " not in username.strip()


def is_email_valid(email):
    """Return True if `email` is a valid email address."""
    if not email or not isinstance(email, str):
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email.strip()) is not None


def is_date_valid(date_str):
    """Return True if `date_str` is in YYYY-MM-DD format."""
    if not date_str or not isinstance(date_str, str):
        return False
    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(date_regex, date_str.strip()) is not None
