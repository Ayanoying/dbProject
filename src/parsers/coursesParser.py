import csv
from utils.validators import is_in_faculty_set


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
                course_code = (row.get("code_cours") or "").strip()
                course_name = (row.get("nom") or "").strip()
                faculty = (row.get("faculte") or "").strip()
                credits_text = (row.get("credits") or "").strip()
                credits = int(credits_text) if credits_text else 5
                courses.append(
                    {
                        "course_code": course_code,
                        "course_name": f"{course_code} - {course_name}"
                        if course_code and course_name
                        else course_name,
                        "faculty": faculty if is_in_faculty_set(faculty) else "Unknown",
                        "credits": credits,
                        "academic_year_id": "2025-2026",
                    }
                )
        return courses

    def get_courses(self):
        """Return loaded courses."""
        return self.data
