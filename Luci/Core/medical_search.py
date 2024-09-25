# Luci/Core/medical_search.py

from Bio import Entrez

class MedicalSearch:
    def __init__(self, email=None):
        """
        Initialize the MedicalSearch class.

        Args:
            email (str): Email address required by NCBI to use Entrez API.
        """
        if not email:
            raise ValueError("Email is required by NCBI to use Entrez API. Please provide a valid email.")
        self.email = email
        Entrez.email = self.email

    def search_pubmed(self, query, max_results=10):
        """
        Search PubMed with a query.

        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to retrieve.

        Returns:
            list: List of PubMed IDs matching the query.
        """
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            results = Entrez.read(handle)
            handle.close()
            id_list = results['IdList']
            return id_list
        except Exception as e:
            print(f"An error occurred during PubMed search: {e}")

    def fetch_articles(self, id_list):
        """
        Fetch articles from PubMed given a list of IDs.

        Args:
            id_list (list): List of PubMed IDs.

        Returns:
            list: List of article details.
        """
        ids = ','.join(id_list)
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        articles = []
        
        try:
            for record in records['PubmedArticle']:
                article = {}
                article['PMID'] = record['MedlineCitation']['PMID']
                article['Title'] = record['MedlineCitation']['Article']['ArticleTitle']
                article['Abstract'] = record['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', [''])[0]
                article['Authors'] = [
                    f"{author.get('LastName', '')} {author.get('ForeName', '')}"
                    for author in record['MedlineCitation']['Article'].get('AuthorList', [])
                ]
                article['Journal'] = record['MedlineCitation']['Article']['Journal']['Title']
                articles.append(article)
            return articles
        except Exception as e:
            print(f"An error occurred during Fetch Articles: {e}")

    def get_articles(self, query, max_results=10):
        """
        Search PubMed and retrieve articles based on a query.

        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to retrieve.

        Returns:
            list: List of article details.
        """
        id_list = self.search_pubmed(query, max_results)
        articles = self.fetch_articles(id_list)
        return articles
