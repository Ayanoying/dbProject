from repositories.specialQueriesRepository import SpecialQueriesRepository


class SpecialQueriesService:
    """Business logic for additional queries."""

    AVAILABLE_QUERIES = {
        "1. Top 10 des utilisateurs avec le plus de points": "get_top_users_by_points",
        "2. Utilisateurs avec des résumés dans au moins 3 cours": "get_users_with_summaries_in_multiple_courses",
        "3. Cours avec le plus de résumé": "get_course_with_most_summaries",
        "4. Meilleur résumé par cours": "get_best_summary_by_course",
        "5. Utilisateurs sans résumés": "get_users_without_summaries",
        "6. Objet cosmétique le plus acheté": "get_most_purchased_cosmetic_item",
        "7. Utilisateurs qui ont dépensé plus que ce qu'ils n'ont": "get_users_who_spent_more_than_have",
        "8. Nombre moyen de résumés par utilisateur": "get_average_summaries_per_user",
    }

    # Mapping of query method names to their expected column headers
    # In french because the whole app is in french - standardisation
    HEADER_MAP = {
        "get_top_users_by_points": [
            "ID utilisateur",
            "Nom d'utilisateur",
            "Points",
        ],
        "get_users_with_summaries_in_multiple_courses": [
            "ID utilisateur",
            "Nom d'utilisateur",
        ],
        "get_course_with_most_summaries": [
            "ID cours",
            "Titre cours",
            "Nombre de résumés",
        ],
        "get_best_summary_by_course": [
            "ID résumé",
            "Titre",
            "ID cours",
            "Note moyenne du meilleur résumé",
        ],
        "get_users_without_summaries": ["ID utilisateur", "Nom d'utilisateur"],
        "get_most_purchased_cosmetic_item": [
            "ID objet",
            "Nom objet",
            "Nombre d'achats",
        ],
        "get_users_who_spent_more_than_have": [
            "ID utilisateur",
            "Nom d'utilisateur",
            "Points",
            "Dépenses totales",
        ],
        "get_average_summaries_per_user": ["Nombre moyen de résumés"],
    }

    def __init__(self):
        self.repo = SpecialQueriesRepository()

    def get_available_queries(self):
        """Return the list of available query names for the dropdown."""
        return self.AVAILABLE_QUERIES

    def execute_query(self, query_method_name):
        """Execute a query by method name and return results with headers."""
        method = getattr(self.repo, query_method_name, None)
        if not method or not callable(method):
            raise ValueError(f"Unknown query method: {query_method_name}")

        rows = method()

        # Get headers based on the query method
        headers = self._get_headers_for_query(query_method_name)

        return headers, rows

    def _get_headers_for_query(self, query_method_name):
        """Return header map which contains header for each query."""

        return self.HEADER_MAP.get(query_method_name, [])
