from repositories.coursesRepository import CoursesRepository


class CoursesService:
    def __init__(self):
        self.repo = CoursesRepository()
