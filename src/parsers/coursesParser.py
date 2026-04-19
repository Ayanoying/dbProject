import csv


class CoursesParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        courses = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["credits"] = int(row["credits"])
                courses.append(row)
        return courses

    def get_courses(self):
        return self.data
    