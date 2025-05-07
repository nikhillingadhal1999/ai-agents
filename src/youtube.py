import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_first_youtube_link(query):
    # Encode query
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Mimic a browser to avoid bot detection
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch search results: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Find first video link
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/watch?v="):
            return "https://www.youtube.com" + href

    return None

# Example usage
if __name__ == "__main__":
    search_term = input("Search YouTube for: ")
    video_link = get_first_youtube_link(search_term)
    if video_link:
        print("First video link:", video_link)
    else:
        print("No video found.")