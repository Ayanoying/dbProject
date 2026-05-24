from defusedxml import ElementTree as ET  # defusedxmlis a safe XML parser
from utils.validators import (
    is_created_username_valid,
    is_email_valid,
    is_date_valid,
    is_level_valid,
    is_positive_int,
)


class UsersParser:
    """Parse users XML into repository-ready dictionaries."""

    def __init__(self, xml_path):
        """Load XML content immediately."""
        self.xml_path = xml_path
        self.data = self._load()

    def _load(self):
        """Return parsed user dictionaries."""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        users = []
        verify_user_uniqueness = set()

        for u in root.findall("utilisateur"):
            if u not in verify_user_uniqueness:
                username = (u.findtext("nomUtilisateur") or "").strip()
                email = (u.findtext("email") or "").strip()
                registration_date = (u.findtext("dateInscription") or "").strip()
                profile_level_str = (u.findtext("niveau") or "").strip()
                profile_points_str = (u.findtext("points") or "").strip()

                if False in (
                    is_created_username_valid(username),
                    is_email_valid(email),
                    is_date_valid(registration_date),
                    is_level_valid(profile_level_str),
                    is_positive_int(profile_points_str),
                ):
                    continue

                users.append(
                    {
                        "username": username,
                        "email": email,
                        "registration_date": registration_date,
                        "profile_level": int(profile_level_str),
                        "profile_points": int(profile_points_str),
                    }
                )
                verify_user_uniqueness.add(u)
        return users

    def get_users(self):
        """Return loaded users."""
        return self.data
