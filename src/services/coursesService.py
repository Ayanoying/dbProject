from repositories.coursesRepository import CoursesRepository


# Ce que le user peut faire avec les cours 

class CoursesService:
    def __init__(self): 
        self.repo = CoursesRepository() # créer une instance du repositery pour pouvoir accéder à la base 

    def lister_cours(self):
        cours = self.repo.get_all() # appelle get_all en affichant un tableau formaté dans le terminal 
        if not cours:
            print("Aucun cours disponible.")
            return
        print(f"\n{'Code':<12} {'Nom':<45} {'Faculté':<20} {'Crédits'}")
        print("-" * 90)
        for c in cours:
            print(f"{c[0]:<12} {c[1]:<45} {c[2]:<20} {c[3]}")

    def ajouter_cours(self, code_cours, nom, faculte, credits):
        inserted = self.repo.add_course(code_cours, nom, faculte, credits) # appellle add_courses et affiche un message de succès ou d'erreur selon si le code etait deja pris 
        if inserted: 
            print(f"Cours '{code_cours}' ajouté avec succès.")
        else:
            print(f"Erreur : le code cours '{code_cours}' existe déjà.")