import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file

from job_monitor.domain.models import SearchCriteria
from job_monitor.pipeline import run_pipeline

DATA_ROOT = Path("data").resolve()
LOG_ROOT = Path("logs")
LOG_ROOT.mkdir(exist_ok=True)
DATA_ROOT.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_ROOT / "job_monitor.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def _safe_data_file_path(relative_path: str) -> Path:
    candidate = (DATA_ROOT / relative_path).resolve()
    if not str(candidate).startswith(str(DATA_ROOT)):
        raise ValueError("Invalid file path")
    return candidate


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    email = (request.form.get("linkedin_email") or "").strip()
    password = request.form.get("linkedin_password") or ""
    role = (request.form.get("role") or "").strip()
    location = (request.form.get("location") or "").strip()
    days_raw = (request.form.get("days") or "2").strip()

    if not role:
        return render_template("index.html", error="Role is required.")

    try:
        days = int(days_raw)
        if days < 0:
            raise ValueError("Days must be non-negative")
    except ValueError:
        return render_template("index.html", error="Days must be a non-negative integer.")

    run_folder = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = DATA_ROOT / run_folder

    try:
        criteria = SearchCriteria(role=role, location=location, days=days)
        csv_path, html_path = run_pipeline(
            criteria=criteria,
            output_dir=str(output_dir),
            headless=True,
            linkedin_email=email or None,
            linkedin_password=password or None,
        )
    except Exception as exc:
        logger.exception("Report generation failed")
        return render_template("index.html", error=f"Failed to generate report: {exc}")

    csv_relative = Path(csv_path).resolve().relative_to(DATA_ROOT).as_posix()
    html_relative = Path(html_path).resolve().relative_to(DATA_ROOT).as_posix()
    return render_template(
        "index.html",
        success=True,
        csv_relative=csv_relative,
        html_relative=html_relative,
        role=role,
        location=location,
        days=days,
    )


@app.get("/download")
def download():
    relative_path = request.args.get("file", "")
    if not relative_path:
        return "Missing file query parameter.", 400

    try:
        file_path = _safe_data_file_path(relative_path)
    except ValueError:
        return "Invalid file path.", 400

    if not file_path.exists() or not file_path.is_file():
        return "File not found.", 404

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=False)

