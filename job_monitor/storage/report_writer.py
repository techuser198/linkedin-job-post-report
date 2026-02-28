import logging
import os
from datetime import datetime

import pandas as pd

from job_monitor.domain.models import JobPost

logger = logging.getLogger(__name__)

REPORT_COLUMNS = [
    "text",
    "post_url",
    "source",
    "matched_role",
    "matched_location",
    "timestamp_scraped",
    "inferred_post_age_days",
]


def write_reports(posts: list[JobPost], output_dir: str) -> tuple[str, str]:
    os.makedirs(output_dir, exist_ok=True)

    rows = [post.to_record() for post in posts]
    df = pd.DataFrame(rows, columns=REPORT_COLUMNS).drop_duplicates(subset=["text"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"report_{timestamp}.csv")
    html_path = os.path.join(output_dir, f"report_{timestamp}.html")

    df.to_csv(csv_path, index=False)
    df.to_html(html_path, index=False)

    logger.info("Reports generated: %s, %s", csv_path, html_path)
    return csv_path, html_path

