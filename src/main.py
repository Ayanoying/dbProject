from parsers.evaluationsParser import EvaluationsParser
from parsers.coursesParser import CoursesParser
from repositories.coursesRepository import CoursesRepository
from repositories.evaluationsRepository import EvaluationsRepository


def main():
    # parsers
    courses_parser = CoursesParser("../res/data/cours.csv")
    evaluations_parser = EvaluationsParser("../res/data/commentaires.json")

    #testing parsers
    courses = courses_parser.get_courses()
    evaluations = evaluations_parser.get_evaluations()

    # db layers
    course_repo = CoursesRepository()
    eval_repo = EvaluationsRepository()

    # insert into DB
    course_repo.save_many(courses)
    eval_repo.save_many(evaluations)


if __name__ == "__main__":
    main()
