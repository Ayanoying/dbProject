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
            users.append(
                {
                    "username": (u.findtext("nomUtilisateur") or "").strip(),
                    "email": (u.findtext("email") or "").strip(),
                    "registration_date": u.findtext("dateInscription"),
                    "profile_level": int(u.findtext("niveau") or 1),
                    "profile_points": int(u.findtext("points") or 0),
                }
            )
        return users

    def get_users(self):
        """Return loaded users."""
        return self.data
