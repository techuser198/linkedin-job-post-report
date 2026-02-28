from playwright.sync_api import Page
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
import logging

logger = logging.getLogger(__name__)

def login(page: Page):
    logger.info("Opening LinkedIn login page")
    page.goto("https://www.linkedin.com/login")

    page.fill("#username", LINKEDIN_EMAIL)
    page.fill("#password", LINKEDIN_PASSWORD)

    page.click("button[type='submit']")
    page.wait_for_selector("input[placeholder='Search']", timeout=20000)

    logger.info("Login successful")
