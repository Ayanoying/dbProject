import xml.etree.ElementTree as ET

class SummariesParser:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.data = self._load()

    def _load(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        summaries = []

        for u in root.findall('utilisateur'):
            author = (u.findtext('nomUtilisateur') or '').strip()
            summaries_node = u.find('resumes')

            if not author or summaries_node is None:
                continue

            for r in summaries_node.findall('resume'):
                course = (r.findtext('cours') or '').strip()
                title = (r.findtext('titre') or '').strip()
                publication_date = (r.findtext('datePublication') or '').strip()
                note_txt = (r.findtext('noteMoyenne') or '').strip()

                if not course or not title:
                    continue

                average_note = float(note_txt) if note_txt else None

                summaries.append({
                    "auteur": author,
                    "cours": course,
                    "titre": title,
                    "date_publication": publication_date if publication_date else None,
                    "note_moyenne": average_note
                })

        return summaries

    def get_summaries(self):
        return self.data
    