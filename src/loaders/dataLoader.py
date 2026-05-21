import os

from parsers.coursesParser import CoursesParser
from parsers.evaluationsParser import EvaluationsParser
from parsers.usersParser import UsersParser
from parsers.summariesParser import SummariesParser

from repositories.coursesRepository import CoursesRepository
from repositories.evaluationsRepository import EvaluationsRepository
from repositories.usersRepository import UsersRepository
from repositories.summariesRepository import SummariesRepository


BASE_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "res", "data")
COURSE_FILE = os.path.join(BASE_DATA, "cours.csv")
USERS_FILE = os.path.join(BASE_DATA, "utilisateurs.xml")
SUMMARIES_FILE = os.path.join(BASE_DATA, "utilisateurs.xml")
EVALUATIONS_FILE = os.path.join(BASE_DATA, "commentaires.json")


def init_data():
    # Parsers
    courses_parser = CoursesParser(COURSE_FILE)
    users_parser = UsersParser(USERS_FILE)
    summaries_parser = SummariesParser(SUMMARIES_FILE)
    evaluations_parser = EvaluationsParser(EVALUATIONS_FILE)

    # Repositories
    courses_repo = CoursesRepository()
    users_repo = UsersRepository()
    summaries_repo = SummariesRepository()
    evaluations_repo = EvaluationsRepository()

    # Insertions
    courses_repo.save_many(courses_parser.get_courses())
    users_repo.save_many(users_parser.get_users())
    summaries_repo.save_many(summaries_parser.get_summaries())
    evaluations_repo.save_many(evaluations_parser.get_evaluations())
