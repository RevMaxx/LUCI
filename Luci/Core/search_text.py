import requests
import aiohttp

async def search_text_async(query, max_results=10):
    """
    Search for a query using a text search API.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of search results, where each result is a dictionary containing 'title', 'href', and 'body'.
    """
    base_url = "https://cerina-search.vercel.app/search"
    params = {
        "q": query,
        "max_results": max_results
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("results", [])
            else:
                raise Exception(f"Failed to fetch results. Status code: {response.status}")


def search_text(query, max_results=10):
    """
    Search for a query using a text search API.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of search results, where each result is a dictionary containing 'title', 'href', and 'body'.
    """
    base_url = "https://cerina-search.vercel.app/search"
    params = {
        "q": query,
        "max_results": max_results
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        raise Exception(f"Failed to fetch results. Status code: {response.status_code}")
    

def print_text_result(results):
    """
    Print the search results.

    Args:
        results (list): List of search results.
    """
    for index, result in enumerate(results, start=1):
        print(f"Result {index}:")
        for key, value in result.items():
            print(f"  {key.capitalize()}: {value}")
        print()
