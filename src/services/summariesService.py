from repositories.summariesRepository import SummariesRepository
from repositories.usersRepository import UsersRepository
from repositories.coursesRepository import CoursesRepository
from repositories.pointsRepository import PointsRepository
from repositories.evaluationsRepository import EvaluationsRepository


class SummariesService:
    """Business logic for summaries and evaluations."""

    def __init__(self):
        self.repo = SummariesRepository()
        self.users_repo = UsersRepository()
        self.courses_repo = CoursesRepository()
        self.points_repo = PointsRepository()
        self.evaluations_repo = EvaluationsRepository()

    def publish(self, username, course_code, title, description):
        """Publish a summary and grant summary points."""
        user = self.users_repo.find_by_username(username)
        if not user:
            return None

        title = (title or "").strip()
        description = (description or "").strip()
        course_code = (course_code or "").strip()

        if not title or not description:
            return "invalid_fields"

        courses = self.courses_repo.get_all()
        codes = [c[1] for c in courses]
        if course_code not in codes:
            return False

        user_id = user[0]
        summary_id = self.repo.publish(title, description, user_id, course_code)
        if summary_id is None:
            return False

        self.points_repo.add_transaction("gain_summary", +50, user_id, summary_id)
        return summary_id

    def see_course_summaries(self, course_code):
        """Return visible summaries for one course."""
        return self.repo.get_by_course(course_code)

    def see_my_summaries(self, username):
        """Return summaries authored by the given user."""
        user = self.users_repo.find_by_username(username)
        if not user:
            return None
        return self.repo.get_by_user(user[0])

    def edit(self, username, summary_id, title, description):
        """Update one summary if the username owns it."""
        user = self.users_repo.find_by_username(username)
        if not user:
            return False
        return self.repo.update(summary_id, title, description, user[0])

    def delete(self, username, summary_id):
        """Delete one summary if the username owns it."""
        user = self.users_repo.find_by_username(username)
        if not user:
            return False

        deleted = self.repo.delete(summary_id, user[0])
        return deleted

    def evaluate(self, username, summary_id, note, comment):
        """Create an evaluation and grant points to the summary author."""
        user = self.users_repo.find_by_username(username)
        if not user:
            return None

        summary = self.repo.get_by_id(summary_id)
        if not summary:
            return False

        if note < 0 or note > 5:
            return "invalid_note"

        evaluation_id = self.evaluations_repo.add_evaluation(
            note, comment, user[0], summary_id
        )
        if evaluation_id == -1:
            return "already_exists"

        self.evaluations_repo.update_summary_average(summary_id)

        summary_author_id = summary[3]
        self.points_repo.add_transaction(
            "gain_evaluation", +10, summary_author_id, summary_id, evaluation_id
        )
        return evaluation_id
