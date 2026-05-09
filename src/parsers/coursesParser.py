import csv

# Rôle : lire le fichier cours.csv et le convertir en liste Python.

class CoursesParser:
    def __init__(self, file_path): # recoit le chemin vers le fichier CSV & déclenche le chargement 
        self.file_path = file_path
        self.data = self._load() # charge les données en mémoire dès la création de l'objet

    def _load(self):
        courses = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f) #Lit chaque ligne du CSV comme un dictionnaire
            for row in reader:
                row["credits"] = int(row["credits"]) # Convertit la colonne crédits de texte en nombre entier
                courses.append(row)
        return courses

    def get_courses(self): #Expose la liste chargée à l'extérieur de la classe
        return self.data
    