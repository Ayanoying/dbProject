from repositories.resumesRepository import ResumesRepository
from repositories.usersRepository import UsersRepository
from repositories.coursesRepository import CoursesRepository

class ResumesService: 
    def __init__(self): # créer 3 instances de repositories 
        self.repo = ResumesRepository()
        self.users_repo = UsersRepository() # pour vérifier sir le nom existe 
        self.course_repo = CoursesRepository() # pour verifier que le code cours est valide 

    def publier(self, nom_utilisateur, code_cours, titre, description):
        user = self.users_repo.find_by_username(nom_utilisateur) # vérifier que le user existe 
        if not user: 
            print(f"Erreur : utilisateur '{nom_utilisateur}' introuvable.")
            return None
        
        cours = self.course_repo.get_all() # vérifie que le cours existe 
        codes = [c[0] for c in cours]
        if code_cours not in codes: 
            print(f"Erreur : le cours '{code_cours}' n'existe pas. ")
            return 
        
        id_utilisateur = user[0]
        id_resume = self.repo.publish(titre, description, id_utilisateur, code_cours)
        print(f"Résumé publié avec succès ! (id: {id_resume})")
        return id_resume

    def voir_resumes_cours(self, code_cours): # Affiche tous les résumés d'un cours avec leur note moyenne si disponible
        resumes = self.repo.get_by_course(code_cours)
        if not resumes: 
            print(f"Aucun résumé pour le cours '{code_cours}'.")
            return 
        
        print(f" \n-- Résumés du cours {code_cours} --")
        for r in resumes:
            note = r[5] if r[5] is not None else "Rien"
            print(f"[{r[0]}] {r[1]} — par {r[6]} | {r[3]} | v{r[4]} | note: {note}")
            if r[2]:
                print(f"{r[2][:80]}...")
    
    def voir_mes_resumes(self, nom_utilisateur): # Trouve l'ID de l'utilisateur par son nom, puis liste ses résumés
        user = self.users_repo.find_by_username(nom_utilisateur)
        if not user:
            print(f"Utilisateur '{nom_utilisateur}' introuvable.")
            return 
        
        resumes = self.repo.get_by_user(user[0])
        if not resumes : 
            print("Vous n'avez publié aucun résumé.")
            return

        print(f"\n-- Résumés de {nom_utilisateur} --")
        for resume in resumes: 
            note = resume[5] if resume[5] is not None else "Rien"
            print(f"[{resume[0]}] {resume[1]} | {resume[2]} | {resume[3]} | v{resume[4]} | note: {note}") # informations du résumé 


    def modifier(self, nom_utilisateur, id_resume, titre, description):
        user = self.users_repo.find_by_username(nom_utilisateur) # vérifie que l'utilisateur existe 
        if not user : 
            print(f"Utilisateur {nom_utilisateur} introuvable.")
            return

        ok = self.repo.update(id_resume, titre, description , user[0]) # tente de mettre à jour le résumé 
        if ok:
            print(f"Résumé {id_resume} mis à jour (version incrémentée).")
        else: # si le résumé n'appartient pas à cet utilisateur 
            print("Modification impossible : résumé introuvable ou vous n'en êtes pas l'auteur.")


    def supprimer(self, nom_utilisateur, id_resume):
        user = self.users_repo.find_by_username(nom_utilisateur) # vérifie l'utilisateur 
        if not user: 
            print(f"Uitlisateur ({nom_utilisateur} introuvable.)")
            return
        
        ok = self.repo.delete(id_resume, user[0]) # tente la suppresion 
        if ok :
            print(f"Résumé {id_resume} supprimé.")
        else:
            print("Suppression impossible : résumé introuvable ou vous n'en êtes pas l'auteur.")
