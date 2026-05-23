from defusedxml import ElementTree as ET


class SummariesParser:
    """Parse summaries XML data from user files."""

    def __init__(self, xml_path, course_lookup=None):
        """Load XML content immediately."""
        self.xml_path = xml_path
        self.course_lookup = course_lookup or {}
        self.data = self._load()

    def _load(self):
        """Return parsed summaries as dictionaries."""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        summaries = []

        for u in root.findall("utilisateur"):
            author = (u.findtext("nomUtilisateur") or "Auteur inconnu").strip()
            summaries_node = u.find("resumes")

            if not author or summaries_node is None:
                continue

            for r in summaries_node.findall("resume"):
                course = (r.findtext("cours") or "Cours inconnu").strip()
                title = (r.findtext("titre") or "Titre inconnu").strip()
                publication_date = (
                    r.findtext("datePublication") or "Date de publication inconnue"
                ).strip()
                average_note = (r.findtext("noteMoyenne") or "Note inconnue").strip()

                summaries.append(
                    {
                        "author": author,
                        "course": self.course_lookup.get(course, course),
                        "title": title,
                        "description": "Aucune description",  # Static because not provided in XML
                        "publication_date": publication_date
                        if publication_date
                        else None,
                        "average_rating": float(average_note)
                        if average_note.replace(".", "", 1).isdigit()
                        else average_note,
                    }
                )

        return summaries

    def get_summaries(self):
        """Return loaded summaries."""
        return self.data
