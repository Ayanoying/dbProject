import xml.etree.ElementTree as ET

class ResumesParser:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.data = self._load()

    def _load(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        resumes = []

        for u in root.findall('utilisateur'):
            auteur = (u.findtext('nomUtilisateur') or '').strip()
            resumes_node = u.find('resumes')

            if not auteur or resumes_node is None:
                continue

            for r in resumes_node.findall('resume'):
                cours = (r.findtext('cours') or '').strip()
                titre = (r.findtext('titre') or '').strip()
                date_publication = (r.findtext('datePublication') or '').strip()
                note_txt = (r.findtext('noteMoyenne') or '').strip()

                if not cours or not titre:
                    continue

                note_moyenne = float(note_txt) if note_txt else None

                resumes.append({
                    "auteur": auteur,
                    "cours": cours,
                    "titre": titre,
                    "date_publication": date_publication if date_publication else None,
                    "note_moyenne": note_moyenne
                })

        return resumes

    def get_resumes(self):
        return self.data