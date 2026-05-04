from parsers.coursesParser import CoursesParser
from parsers.evaluationsParser import EvaluationsParser
from parsers.usersParser import UsersParser
from repositories.coursesRepository import CoursesRepository
from repositories.evaluationsRepository import EvaluationsRepository
from repositories.usersRepository import UsersRepository
from services.usersService import UsersService


def charger_donnees():
    # Parsers
    courses_parser    = CoursesParser("../res/data/cours.csv")
    evaluations_parser = EvaluationsParser("../res/data/commentaires.json")
    users_parser      = UsersParser("../res/data/utilisateurs.xml")

    # Repositories
    course_repo = CoursesRepository()
    eval_repo   = EvaluationsRepository()
    users_repo  = UsersRepository()

    # Insertion dans la base
    course_repo.save_many(courses_parser.get_courses())
    users_repo.save_many(users_parser.get_users())
    eval_repo.save_many(evaluations_parser.get_evaluations())

    print("Données chargées avec succès.")


def menu_utilisateurs(service):
    while True:
        print("\n--- Gestion des utilisateurs ---")
        print("1. S'inscrire")
        print("2. Se connecter")
        print("3. Voir un profil")
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
        elif choix == "0":
            break


def main():
    users_service = UsersService()

    while True:
        print("\n=== Plateforme de résumés ===")
        print("1. Gestion des utilisateurs")
        print("2. Charger les données initiales")
        print("0. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            menu_utilisateurs(users_service)
        elif choix == "2":
            charger_donnees()
        elif choix == "0":
            print("Au revoir !")
            break


if __name__ == "__main__":
    main()


# charge les données quand on lance l'appli 