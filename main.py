import argparse
import logging
import os

from job_monitor.domain.models import SearchCriteria
from job_monitor.pipeline import run_pipeline

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/job_monitor.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def main():
    arg_parser = argparse.ArgumentParser(description="LinkedIn Job Monitor")
    arg_parser.add_argument("--role", required=True, help="Job role keyword")
    arg_parser.add_argument("--location", default="", help="Location keyword (e.g. Dubai)")
    arg_parser.add_argument("--days", type=int, default=2, help="Time window in days")
    arg_parser.add_argument("--output", default="data", help="Output directory")
    arg_parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    args = arg_parser.parse_args()

    criteria = SearchCriteria(role=args.role, location=args.location, days=args.days)
    csv_path, html_path = run_pipeline(criteria=criteria, output_dir=args.output, headless=args.headless)
    logging.info("Run complete. CSV=%s HTML=%s", csv_path, html_path)
    print(f"Saved reports:\n- {csv_path}\n- {html_path}")

if __name__ == "__main__":
    main()
