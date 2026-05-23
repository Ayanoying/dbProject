from repositories.coursesRepository import CoursesRepository
from utils.validators import is_in_faculty_set, is_valid_course_code


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

        if not course_code or not course_title or not faculty or not academic_year_id:
            return "missing_fields"

        if not is_valid_course_code(course_code):
            return "invalid_course_code"
        if not is_in_faculty_set(faculty):
            return "invalid_faculty"
        inserted = self.repo.add_course(
            course_code, course_title, faculty, academic_year_id
        )
        if not inserted:
            return "already_exists"
        return inserted
