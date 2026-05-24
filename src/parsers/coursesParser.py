import csv
from utils.validators import is_faculty_valid, is_credits_valid, is_course_code_valid

DEFAULT_ACADEMIC_YEAR = "2025-2026"
DEFAULT_COURSE_TITLE = "Titre de cours inconnu"


class CoursesParser:
    """Parse courses CSV data for database insertion."""

    def __init__(self, file_path):
        """Load CSV content immediately."""
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        """Return parsed courses as dictionaries matching repository expectations."""
        courses = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                course_code_str = (row.get("code") or "").strip()
                course_title_str = (row.get("nom") or DEFAULT_COURSE_TITLE).strip()
                faculty_str = (row.get("faculte") or "").strip()
                credits_str = (row.get("credits") or "").strip()

                if False in (
                    is_faculty_valid(faculty_str),
                    is_credits_valid(credits_str),
                    is_course_code_valid(course_code_str),
                ):
                    continue

                courses.append(
                    {
                        "course_code": course_code_str,
                        "course_title": course_title_str,
                        "faculty": faculty_str,
                        "credits": int(credits_str),
                        "academic_year_id": DEFAULT_ACADEMIC_YEAR,  # Static value because not provided in CSV
                    }
                )
        return courses

    def get_courses(self):
        """Return loaded courses."""
        return self.data
