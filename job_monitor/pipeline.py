import logging

from playwright.sync_api import sync_playwright

from job_monitor.domain.models import SearchCriteria
from job_monitor.extractors.linkedin_post_extractor import extract_posts
from job_monitor.filters.post_filters import filter_posts
from job_monitor.providers.linkedin_content_provider import LinkedInContentProvider
from job_monitor.storage.report_writer import write_reports

logger = logging.getLogger(__name__)


def run_pipeline(
    criteria: SearchCriteria,
    output_dir: str,
    headless: bool = False,
    linkedin_email: str | None = None,
    linkedin_password: str | None = None,
) -> tuple[str, str]:
    provider = LinkedInContentProvider()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = browser.new_page()

        provider.login(page, email=linkedin_email, password=linkedin_password)
        html = provider.fetch_posts_html(page, criteria)

        browser.close()

    extracted_posts = extract_posts(html, criteria)
    filtered_posts = filter_posts(extracted_posts, criteria)
    report_paths = write_reports(filtered_posts, output_dir)

    logger.info(
        "Pipeline complete. query='%s' extracted=%s filtered=%s",
        criteria.query,
        len(extracted_posts),
        len(filtered_posts),
    )
    return report_paths
