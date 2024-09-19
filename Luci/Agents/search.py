from Luci.Core.search_text import search_text_async, search_text, print_text_result
from Luci.Core.search_image import search_images_async, search_images, print_img_result

class Search:
    def __init__(self, query: str):
        self.query = query

    async def search_text_async(self, max_results=10):
        """
        Perform an asynchronous text search using the query provided.

        Args:
            max_results (int): The maximum number of results to fetch.

        Returns:
            list: A list of search results.
        """
        return await search_text_async(self.query, max_results)

    def search_text(self, max_results=10):
        """
        Perform a synchronous text search using the query provided.

        Args:
            max_results (int): The maximum number of results to fetch.

        Returns:
            list: A list of search results.
        """
        return search_text(self.query, max_results)

    async def search_images_async(self, max_results=10):
        """
        Perform an asynchronous image search using the query provided.

        Args:
            max_results (int): The maximum number of results to fetch.

        Returns:
            list: A list of image search results.
        """
        return await search_images_async(self.query, max_results)

    def search_images(self, max_results=10):
        """
        Perform a synchronous image search using the query provided.

        Args:
            max_results (int): The maximum number of results to fetch.

        Returns:
            list: A list of image search results.
        """
        return search_images(self.query, max_results)

    def print_text_result(self, results):
        """
        Print the text search results.

        Args:
            results (list): List of search results.
        """
        print_text_result(results)

    def print_img_result(self, results):
        """
        Print the image search results.

        Args:
            results (list): List of image search results.
        """
        print_img_result(results)
