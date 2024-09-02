import requests
import aiohttp
import asyncio

async def search_images_async(query, max_results=5):
    """
    Search for images using a search API.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of image search results, where each result is a dictionary containing 'title', 'url', 'image', 'thumbnail', 'source', 'width', and 'height'.
    """
    base_url = "https://cerina-search.vercel.app/searchImages"
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

def search_images(query, max_results=5):
    """
    Search for images using a search API.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of image search results, where each result is a dictionary containing 'title', 'url', 'image', 'thumbnail', 'source', 'width', and 'height'.
    """
    base_url = "https://cerina-search.vercel.app/searchImages"
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

def print_img_result(results):
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