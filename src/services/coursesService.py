from repositories.coursesRepository import CoursesRepository


class CoursesService:
    def __init__(self):
        self.repo = CoursesRepository()  # creates a repository instance

    def list_courses(self):
        courses = self.repo.get_all()
        return courses

    def add_courses(self, course_code, name, faculty, credits):
        inserted = self.repo.add_course(course_code, name, faculty, credits)
        return inserted
