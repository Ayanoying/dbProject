from repositories.coursesRepository import CoursesRepository
from utils.validators import is_faculty_valid, is_course_code_valid, is_date_valid


class CoursesService:
    """Business logic for courses."""

    def __init__(self):
        self.repo = CoursesRepository()

    def list_courses(self):
        """Return all courses."""
        courses = self.repo.get_all()
        return courses

    def add_course(self, course_code, course_title, faculty, academic_year_id):
        """Create one course and return a status string or True."""
        course_code = (course_code or "").strip()
        course_title = (course_title or "").strip()
        faculty = (faculty or "").strip()
        academic_year_id = (academic_year_id or "").strip()

        if "" in (course_code, course_title, faculty, academic_year_id):
            return "missing_fields"

        if not is_course_code_valid(course_code):
            return "invalid_course_code"
        if not is_faculty_valid(faculty):
            return "invalid_faculty"
        if not is_date_valid(academic_year_id):
            return "invalid_academic_year"
        inserted = self.repo.add_course(
            course_code, course_title, faculty, academic_year_id
        )
        if not inserted:
            return "already_exists"
        return inserted

    def request3(self):
        course = self.repo.additional_request_3()
        return course
