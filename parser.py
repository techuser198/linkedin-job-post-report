from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import re

logger = logging.getLogger(__name__)

def parse_posts(html: str, role: str, days: int, location: str = ""):
    soup = BeautifulSoup(html, "lxml")
    posts_data = []
    cutoff = datetime.utcnow() - timedelta(days=days)

    posts = soup.find_all("div", class_=re.compile("feed-shared-update-v2"))

    for post in posts:
        try:
            text = post.get_text(separator=" ", strip=True)
            if role.lower() not in text.lower():
                continue
            if location and location.lower() not in text.lower():
                continue

            link_tag = post.find("a", href=True)
            post_url = link_tag["href"] if link_tag else ""

            posts_data.append({
                "text": text[:1500],
                "matched_role": role,
                "matched_location": location or "",
                "post_url": post_url,
                "timestamp_scraped": datetime.utcnow().isoformat()
            })

        except Exception as e:
            logger.error(f"Error parsing post: {e}")

    logger.info(f"Parsed {len(posts_data)} posts")
    return posts_data
