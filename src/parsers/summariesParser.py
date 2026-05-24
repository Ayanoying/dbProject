from defusedxml import ElementTree as ET

from utils.validators import is_course_code_valid, is_average_note_valid, is_date_valid

DEFAULT_COURSE_TITLE = "Titre de cours inconnu"
DEFAULT_SUMMARY_DESCRIPTION = "Aucune description"


class SummariesParser:
    """Parse summaries XML data from user files."""

    def __init__(self, xml_path):
        """Load XML content immediately."""
        self.xml_path = xml_path
        self.data = self._load()

    def _load(self):
        """Return parsed summaries as dictionaries."""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        if root is None:
            return []
        summaries = []

        for u in root.findall("utilisateur"):
            author = u.findtext("nomUtilisateur")
            summaries_node = u.find("resumes")

            if not author or summaries_node is None:
                continue

            for r in summaries_node.findall("resume"):
                course_code_str = (r.findtext("cours") or "").strip()
                title_str = (r.findtext("titre") or DEFAULT_COURSE_TITLE).strip()
                publication_date_str = (r.findtext("datePublication") or "").strip()
                average_note_str = (r.findtext("noteMoyenne") or "").strip()

                if False in (
                    is_course_code_valid(course_code_str),
                    is_average_note_valid(average_note_str),
                    is_date_valid(publication_date_str),
                ):
                    continue

                summaries.append(
                    {
                        "author": author,
                        "course_code": course_code_str,
                        "title": title_str,
                        "description": DEFAULT_SUMMARY_DESCRIPTION,  # Static because not provided in XML
                        "publication_date": publication_date_str,
                        "average_rating": float(average_note_str),
                    }
                )

        return summaries

    def get_summaries(self):
        """Return loaded summaries."""
        return self.data
