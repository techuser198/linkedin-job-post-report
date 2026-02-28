import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from job_monitor.domain.models import JobPost, SearchCriteria

logger = logging.getLogger(__name__)

_POST_CONTAINER_PATTERN = re.compile("feed-shared-update-v2")
_AGE_PATTERN = re.compile(r"\b(\d+)\s*([hdwm])\b", re.IGNORECASE)


def _normalize_post_url(url: str) -> str:
    if not url:
        return ""
    if url.startswith("/"):
        return f"https://www.linkedin.com{url}"
    return url


def _infer_post_age_days(text: str) -> int | None:
    match = _AGE_PATTERN.search(text)
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2).lower()

    if unit == "h":
        return 0
    if unit == "d":
        return value
    if unit == "w":
        return value * 7
    if unit == "m":
        return value * 30
    return None


def extract_posts(html: str, criteria: SearchCriteria) -> list[JobPost]:
    soup = BeautifulSoup(html, "lxml")
    raw_posts = soup.find_all("div", class_=_POST_CONTAINER_PATTERN)
    extracted: list[JobPost] = []

    for post in raw_posts:
        try:
            text = post.get_text(separator=" ", strip=True)
            if not text:
                continue

            link_tag = post.find("a", href=True)
            post_url = _normalize_post_url(link_tag["href"]) if link_tag else ""

            extracted.append(
                JobPost(
                    text=text[:1500],
                    post_url=post_url,
                    source="linkedin",
                    matched_role=criteria.role,
                    matched_location=criteria.location,
                    timestamp_scraped=datetime.utcnow().isoformat(),
                    inferred_post_age_days=_infer_post_age_days(text),
                )
            )
        except Exception as exc:
            logger.error("Error extracting post: %s", exc)

    logger.info("Extracted %s raw posts", len(extracted))
    return extracted

