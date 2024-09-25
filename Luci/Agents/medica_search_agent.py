# Luci/Agents/medical_search_agent.py

from Luci.Core.medical_search import MedicalSearch

class MedicalSearchAgent:
    def __init__(self, email=None, max_results=10):
        """
        Initialize the MedicalSearchAgent.

        Args:
            email (str): Email address required by NCBI to use Entrez API.
            max_results (int): Maximum number of results to retrieve.
        """
        if not email:
            raise ValueError("Email is required by NCBI to use Entrez API. Please provide a valid email.")
        self.email = email  # Correctly assign the email
        self.max_results = max_results
        self.medical_search = MedicalSearch(email=self.email)

    def search(self, query):
        """
        Search for articles based on a query.

        Args:
            query (str): The search query.

        Returns:
            list: List of article details.
        """
        articles = self.medical_search.get_articles(query, max_results=self.max_results)
        return articles

    def print_results(self, articles):
        """
        Print the search results.

        Args:
            articles (list): List of article details.
        """
        if not articles:
            print("No articles found for the given query.")
            return

        for idx, article in enumerate(articles):
            print(f"Result {idx+1}:")
            print(f"PMID: {article.get('PMID', 'N/A')}")
            print(f"Title: {article.get('Title', 'N/A')}")
            print(f"Authors: {', '.join(article.get('Authors', []))}")
            print(f"Journal: {article.get('Journal', 'N/A')}")
            print(f"Abstract: {article.get('Abstract', 'N/A')}\n")
