import logging
import urllib.parse

from playwright.sync_api import Page

from job_monitor.domain.models import SearchCriteria
from job_monitor.settings import get_default_linkedin_credentials, validate_linkedin_credentials

logger = logging.getLogger(__name__)


class LinkedInContentProvider:
    def __init__(self, scroll_iterations: int = 5, scroll_pixels: int = 5000) -> None:
        self.scroll_iterations = scroll_iterations
        self.scroll_pixels = scroll_pixels

    def login(self, page: Page, email: str | None = None, password: str | None = None) -> None:
        env_email, env_password = get_default_linkedin_credentials()
        login_email = email or env_email
        login_password = password or env_password
        validate_linkedin_credentials(login_email, login_password)

        logger.info("Opening LinkedIn login page")
        page.goto("https://www.linkedin.com/login")

        page.fill("#username", login_email)
        page.fill("#password", login_password)
        page.click("button[type='submit']")
        page.wait_for_selector("input[placeholder='Search']", timeout=20000)
        logger.info("LinkedIn login successful")

    def fetch_posts_html(self, page: Page, criteria: SearchCriteria) -> str:
        logger.info("Searching LinkedIn content for query: %s", criteria.query)
        encoded_query = urllib.parse.quote(criteria.query)
        search_url = (
            "https://www.linkedin.com/search/results/content/"
            f"?keywords={encoded_query}&origin=GLOBAL_SEARCH_HEADER"
        )

        page.goto(search_url)
        page.wait_for_selector("div.search-results-container", timeout=20000)

        for _ in range(self.scroll_iterations):
            page.mouse.wheel(0, self.scroll_pixels)
            page.wait_for_timeout(1000)

        return page.content()
