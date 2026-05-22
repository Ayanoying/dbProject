import unicodedata


def normalize_data(value):
    """Normalize a string by removing accents and converting to lowercase."""
    normalized = unicodedata.normalize("NFKD", value or "")
    normalized = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    return normalized.strip().lower()
