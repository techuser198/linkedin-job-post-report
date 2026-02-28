import pandas as pd
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_report(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(data).drop_duplicates(subset=["text"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"report_{timestamp}.csv")
    html_path = os.path.join(output_dir, f"report_{timestamp}.html")

    df.to_csv(csv_path, index=False)
    df.to_html(html_path, index=False)

    logger.info("Reports generated")
    return csv_path, html_path
