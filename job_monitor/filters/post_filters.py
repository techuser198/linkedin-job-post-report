import logging

from job_monitor.domain.models import JobPost, SearchCriteria

logger = logging.getLogger(__name__)


def filter_posts(posts: list[JobPost], criteria: SearchCriteria) -> list[JobPost]:
    role = criteria.role.lower().strip()
    location = criteria.location.lower().strip()
    filtered: list[JobPost] = []

    for post in posts:
        text = post.text.lower()

        if role and role not in text:
            continue
        if location and location not in text:
            continue
        if post.inferred_post_age_days is not None and post.inferred_post_age_days > criteria.days:
            continue

        filtered.append(post)

    logger.info("Filtered posts from %s to %s", len(posts), len(filtered))
    return filtered

