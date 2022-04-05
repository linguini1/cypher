# Imports
import requests

# Constants
BASE_URL = "https://newsapi.org/v2/top-headlines"
RESULTS = 6


# Functions
def get_api_key() -> str:

    """Returns the API key."""

    with open("./resources/newsApiKey.txt") as file:
        key = next(file)

    return key


def create_url(category: str | None, key_word: str | None, country: str = "ca") -> str:

    """Returns the URL formatted with the correct parameters."""

    # API key
    key = get_api_key()

    # Category
    category = f"&category={category}" if category else ""

    # Keywords
    if key_word:
        key_word.replace(" ", "%20")  # Format keyword phrase for URL
        key_word = f"&q={key_word}"
    else:
        key_word = ""

    return f"{BASE_URL}?country={country}&apiKey={key}&pageSize={RESULTS}{category}{key_word}"


def get_articles(url: str) -> list:

    """Returns the articles as JSON."""

    results = requests.get(url)
    results = results.json()

    return results["articles"]


def get_titles(articles: list) -> list:

    """Returns the headlines of the top articles."""

    return [article["title"] for article in articles]



