from repositories.evaluationsRepository import EvaluationsRepository


class EvaluationsService:
    def __init__(self):
        self.repo = EvaluationsRepository()
