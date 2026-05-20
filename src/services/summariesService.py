from repositories.summariesRepository import SummariesRepository
from repositories.usersRepository import UsersRepository
from repositories.coursesRepository import CoursesRepository
from repositories.pointsRepository import PointsRepository
from repositories.evaluationsRepository import EvaluationsRepository

class SummariesService:

    def __init__(self):
        self.repo = SummariesRepository()
        self.users_repo = UsersRepository()
        self.courses_repo = CoursesRepository()
        self.points_repo = PointsRepository()
        self.evaluations_repo = EvaluationsRepository()

    def publish(self, username, course_code, title, description):
        user = self.users_repo.find_by_username(username)
        if not user:
            return None
        courses = self.courses_repo.get_all()
        codes = [c[0] for c in courses]
        if course_code not in codes:
            return False
        user_id = user[0]
        summary_id = self.repo.publish(title, description, user_id, course_code)
        self.points_repo.add_transaction('publication', +50, user_id, summary_id)
        return summary_id

    def see_course_summaries(self, course_code):
        return self.repo.get_by_course(course_code)

    def see_my_summaries(self, username):
        user = self.users_repo.find_by_username(username)
        if not user:
            return None
        return self.repo.get_by_user(user[0])

    def edit(self, username, summary_id, title, description):
        user = self.users_repo.find_by_username(username)
        if not user:
            return False
        return self.repo.update(summary_id, title, description, user[0])

    def delete(self, username, summary_id):
        user = self.users_repo.find_by_username(username)
        if not user:
            return False

        deleted = self.repo.delete(summary_id, user[0])
        if not deleted:
            return False

        self.points_repo.add_transaction('suppression', -50, user[0], summary_id = None)
        return True

    def evaluate(self, username, summary_id, note, commentaire):
        user = self.users_repo.find_by_username(username)
        if not user:
            return None

        summaries = self.repo.get_by_id(summary_id)
        if not summaries:
            return False

        if note < 0 or note > 5:
            return "invalid_note"

        evaluation_id = self.evaluations_repo.add_evaluation(
            note,
            commentaire,
            user[0],
            summary_id
        )
        if evaluation_id == -1:
            return "already_exists"
        
        self.evaluations_repo.update_summary_average(summary_id)
        self.points_repo.add_transaction('evaluation', +10, user[0], None, evaluation_id)
        return evaluation_id
