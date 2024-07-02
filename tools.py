import requests
from crewai_tools import tool
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()
# Retrieve the API key from an environment variable
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
print(PEXELS_API_KEY)

@tool("pexels_image_search")
def pexels_image_search(query: str, per_page: Optional[int] = 1) -> str:
    """
    Search for images on Pexels based on a given query.
    
    Args:
    query (str): The search term to find images.
    per_page (int, optional): Number of results to return. Default is 1.

    Returns:
    str: A string representation of a list of dictionaries containing image details.
    """
    if not PEXELS_API_KEY:
        return "Error: Pexels API key not found. Please set the PEXELS_API_KEY environment variable."

    base_url = "https://api.pexels.com/v1/search"
    
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    params = {
        "query": query,
        "per_page": per_page
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        results = []
        for photo in data['photos']:
            results.append({
                'id': photo['id'],
                'width': photo['width'],
                'height': photo['height'],
                'url': photo['url'],
                'photographer': photo['photographer'],
                'src': photo['src']['original']
            })
        
        if not results:
            return "No images found for the given query."
        
        return str(results)

    except requests.exceptions.RequestException as e:
        return f"Error occurred while fetching images: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from Pexels API"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Example usage:
# result = pexels_image_search("nature", 3)
# print(result)