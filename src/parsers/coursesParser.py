import csv
from utils.validators import is_in_faculty_set


DEFAULT_CREDITS = 5


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
                course_code = (row.get("code_cours") or "Code inconnu").strip()
                course_name = (row.get("nom") or "Nom inconnu").strip()
                faculty = (row.get("faculte") or "Faculté inconnue").strip()
                credits_text = (row.get("credits") or "Credits inconnus").strip()
                credits = int(credits_text) if credits_text else DEFAULT_CREDITS
                courses.append(
                    {
                        "course_name": f"{course_code} - {course_name}",
                        "faculty": faculty
                        if is_in_faculty_set(faculty)
                        else "Inconnue",
                        "credits": credits,
                        "academic_year_id": "2025-2026",  # Static value because not provided in CSV
                    }
                )
        return courses

    def get_courses(self):
        """Return loaded courses."""
        return self.data
