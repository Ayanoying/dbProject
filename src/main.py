import os 

from parsers.coursesParser import CoursesParser
from parsers.evaluationsParser import EvaluationsParser
from parsers.usersParser import UsersParser
from parsers.resumesParser import ResumesParser
from repositories.coursesRepository import CoursesRepository
from repositories.evaluationsRepository import EvaluationsRepository
from repositories.usersRepository import UsersRepository
from repositories.resumesRepository import ResumesRepository
from services.usersService import UsersService
from services.coursesService import CoursesService
from services.resumesService import ResumesService


BASE_DATA = os.path.join(os.path.dirname(__file__), "..", "res", "data")

def charger_donnees():
    # Parsers
    courses_parser     = CoursesParser(os.path.join(BASE_DATA, "cours.csv"))
    users_parser       = UsersParser(os.path.join(BASE_DATA, "utilisateurs.xml"))
    resumes_parser     = ResumesParser(os.path.join(BASE_DATA, "utilisateurs.xml"))
    evaluations_parser = EvaluationsParser(os.path.join(BASE_DATA, "commentaires.json"))
  

    # Repositories
    course_repo = CoursesRepository()
    users_repo  = UsersRepository()
    resumes_repo = ResumesRepository()
    eval_repo   = EvaluationsRepository()

    # Insertion dans la base
    course_repo.save_many(courses_parser.get_courses())
    users_repo.save_many(users_parser.get_users())
    resumes_repo.save_many(resumes_parser.get_resumes())
    eval_repo.save_many(evaluations_parser.get_evaluations())

    print("Données chargées avec succès.")


def menu_utilisateurs(service):
    while True:
        print("\n-- Gestion des utilisateurs --")
        print("1. S'inscrire")
        print("2. Se connecter")
        print("3. Voir un profil")
        print("4. Voir l'historique des points")
        print("0. Retour")
        choix = input("Votre choix : ")

        if choix == "1":
            nom   = input("Nom d'utilisateur : ")
            email = input("Email : ")
            service.inscrire(nom, email)
        elif choix == "2":
            nom = input("Nom d'utilisateur : ")
            service.connecter(nom)
        elif choix == "3":
            nom = input("Nom d'utilisateur : ")
            service.voir_profil(nom)
        elif choix == "4":
            nom = input("Nom d'utilisateur : ")
            service.voir_historique_points(nom)
        elif choix == "0":
            break

def menu_cours(service):
    while True:
        print("\n-- Gestion des cours --")
        print("1. Voir la liste des cours")
        print("2. Ajouter un cours")
        print("0. Retour")
        choix = input("Votre choix : ")

        if choix == "1":
            service.lister_cours()
        elif choix == "2":
            code   = input("Code du cours (ex: INFOH303) : ").strip().upper()
            nom    = input("Nom du cours : ").strip()
            fac    = input("Faculté : ").strip()
            try:
                credits = int(input("Crédits : ").strip())
            except ValueError:
                print("Erreur : les crédits doivent être un nombre entier.")
                continue
            service.ajouter_cours(code, nom, fac, credits)
        elif choix == "0":
            break


def menu_resumes(service):
    while True:
        print("\n-- Gestion des résumés --")
        print("1. Voir les résumés d'un cours")
        print("2. Publier un résumé")
        print("3. Voir mes résumés")
        print("4. Modifier un de mes résumés")
        print("5. Supprimer un de mes résumés")
        print("0. Retour")
        choix = input("Votre choix : ")

        if choix == "1":
            code = input("Code du cours : ").strip().upper()
            service.voir_resumes_cours(code)
        elif choix == "2":
            nom   = input("Votre nom d'utilisateur : ").strip()
            code  = input("Code du cours : ").strip().upper()
            titre = input("Titre du résumé : ").strip()
            desc  = input("Description : ").strip()
            service.publier(nom, code, titre, desc)
        elif choix == "3":
            nom = input("Votre nom d'utilisateur : ").strip()
            service.voir_mes_resumes(nom)
        elif choix == "4":
            nom  = input("Votre nom d'utilisateur : ").strip()
            try:
                id_r = int(input("ID du résumé à modifier : "))
            except ValueError:
                print("ID invalide.")
                continue
            titre = input("Nouveau titre : ").strip()
            desc  = input("Nouvelle description : ").strip()
            service.modifier(nom, id_r, titre, desc)
        elif choix == "5":
            nom = input("Votre nom d'utilisateur : ").strip()
            try:
                id_r = int(input("ID du résumé à supprimer : "))
            except ValueError:
                print("ID invalide.")
                continue
            service.supprimer(nom, id_r)
        elif choix == "0":
            break
1
def main():
    users_service   = UsersService()
    courses_service = CoursesService()
    resumes_service = ResumesService()

    while True:
        print("\n== Plateforme de résumés ==")
        print("1. Gestion des utilisateurs")
        print("2. Gestion des cours")
        print("3. Gestion des résumés")
        print("4. Charger les données initiales")
        print("0. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            menu_utilisateurs(users_service)
        elif choix == "2":
            menu_cours(courses_service)
        elif choix == "3":
            menu_resumes(resumes_service)
        elif choix == "4":
            charger_donnees()
        elif choix == "0":
            print("Au revoir !")
            break


if __name__ == "__main__":
    main()


# charge les données quand on lance l'appli 