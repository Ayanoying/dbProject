from defusedxml import ElementTree as ET  # defusedxmlis a safe XML parser


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

        for u in root.findall("utilisateur"):
            username = (
                u.findtext("nomUtilisateur") or "Nom d'utilisateur inconnu"
            ).strip()
            email = (u.findtext("email") or "Email inconnu").strip()
            registration_date = (
                u.findtext("dateInscription") or "Date d'inscription inconnue"
            ).strip()
            profile_level = int(
                u.findtext("niveau") or 1
            )  # Default to level 1 if not provided
            profile_points = int(
                u.findtext("points") or 0
            )  # Default to 0 points if not provided

            users.append(
                {
                    "username": username,
                    "email": email,
                    "registration_date": registration_date,
                    "profile_level": profile_level,
                    "profile_points": profile_points,
                }
            )
        return users

    def get_users(self):
        """Return loaded users."""
        return self.data
