import xml.etree.ElementTree as ET  # bibliothèque Python pour lire des fichiers XML


class UsersParser:
    def __init__(self, xml_path):  # constructeur : reçoit le chemin vers le fichier XML
        self.xml_path = xml_path  # mémorise le chemin
        self.data = self._load()  # charge les données dès la création de l'objet

    def _load(self):
        tree = ET.parse(self.xml_path)  # lit et parse le fichier XML complet
        root = tree.getroot()  # récupère la racine 'utilisateurs'
        users = []  # liste vide qui va stocker tous les utilisateurs
        for u in root.findall("utilisateur"):  # boucle sur chaque utilisateur
            users.append(
                {
                    "nom_utilisateur": u.findtext(
                        "nomUtilisateur"
                    ),  # lit le texte de 'nomUtilisateur'
                    "email": u.findtext("email"),  # lit le texte de 'email'
                    "date_inscription": u.findtext(
                        "dateInscription"
                    ),  # lit la date d'inscription
                    "niveau": int(
                        u.findtext("niveau") or 1
                    ),  # converti en entier, 1 par défaut
                    "nombre_points": int(
                        u.findtext("points") or 0
                    ),  # converti en entier, 0 par défaut
                }
            )
        return users  # retourne la liste de dictionnaires

    def get_users(self):
        return self.data  # permet à l'extérieur de récupérer les données chargées


# Lit les fichiers du dossier data (XML/JSON/CSV) et le transforme en données python
