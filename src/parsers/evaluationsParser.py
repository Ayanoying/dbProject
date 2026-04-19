import json


class EvaluationsParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)["evaluations"]

    def get_evaluations(self):
        return self.data
