from repositories.coursesRepository import CoursesRepository


class CoursesService:
    """Business logic for courses."""

    def __init__(self):
        self.repo = CoursesRepository()

    def list_courses(self):
        """Return all courses."""
        courses = self.repo.get_all()
        return courses

    def add_course(self, course_code, course_title, faculty, academic_year_id):
        """Create one course."""
        inserted = self.repo.add_course(
            course_code, course_title, faculty, academic_year_id
        )
        return inserted
