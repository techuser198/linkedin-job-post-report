from playwright.sync_api import Page
import logging
import urllib.parse

logger = logging.getLogger(__name__)

def search_posts(page: Page, role: str, location: str = ""):
    query = f"{role} {location}".strip()
    logger.info(f"Searching for query: {query}")

    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_query}&origin=GLOBAL_SEARCH_HEADER"

    page.goto(search_url)
    page.wait_for_selector("div.search-results-container", timeout=20000)

    # Scroll to load dynamic content
    for _ in range(5):
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1000)

    return page.content()
