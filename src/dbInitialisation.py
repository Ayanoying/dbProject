import os
from parsers.coursesParser import CoursesParser
from parsers.evaluationsParser import EvaluationsParser
from parsers.usersParser import UsersParser
from parsers.summariesParser import SummariesParser
from parsers.shopParser import ShopParser

from repositories.coursesRepository import CoursesRepository
from repositories.evaluationsRepository import EvaluationsRepository
from repositories.usersRepository import UsersRepository
from repositories.summariesRepository import SummariesRepository
from repositories.shopRepository import ShopRepository


BASE_DATA = os.path.join(os.path.dirname(__file__), "..", "res", "data")
COURSE_FILE = os.path.join(BASE_DATA, "cours.csv")
USERS_FILE = os.path.join(BASE_DATA, "utilisateurs.xml")
SUMMARIES_FILE = os.path.join(BASE_DATA, "utilisateurs.xml")
EVALUATIONS_FILE = os.path.join(BASE_DATA, "commentaires.json")
SHOP_FILE = os.path.join(BASE_DATA, "recompenses.xml")


def init_data():
    """Load seed data into all main tables."""

    courses_parser = CoursesParser(COURSE_FILE)
    users_parser = UsersParser(USERS_FILE)
    evaluations_parser = EvaluationsParser(EVALUATIONS_FILE)
    shop_parser = ShopParser(SHOP_FILE)

    summaries_parser = SummariesParser(SUMMARIES_FILE)
    courses_repo = CoursesRepository()
    users_repo = UsersRepository()
    summaries_repo = SummariesRepository()
    evaluations_repo = EvaluationsRepository()
    shop_repo = ShopRepository()

    courses_repo.save_many(courses_parser.get_courses())
    users_repo.save_many(users_parser.get_users())
    summaries_repo.save_many(summaries_parser.get_summaries())
    evaluations_repo.save_many(evaluations_parser.get_evaluations())
    shop_repo.save_many(shop_parser.get_items())
