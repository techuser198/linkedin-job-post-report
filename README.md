# LinkedIn Job Monitor

This project logs in to LinkedIn, searches content posts by role/location, filters results, and generates CSV + HTML reports.

## Prerequisites

- Python 3.10+
- `pip`
- Chromium browser binaries for Playwright

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Install Playwright Chromium.

```powershell
playwright install chromium
```

4. Create your environment file from example.

```powershell
copy .env.example .env
```

5. Edit `.env` and set:

- `LINKEDIN_EMAIL`
- `LINKEDIN_PASSWORD`

## Run (CLI)

Use `main.py` to run the pipeline from terminal:

```powershell
python main.py --role "python developer" --location "Dubai" --days 2 --headless
```

### CLI options

- `--role` (required): Role or keyword to search.
- `--location` (optional): Location keyword.
- `--days` (optional, default `2`): Time window in days.
- `--output` (optional, default `data`): Output folder.
- `--headless` (optional): Run browser in headless mode.

Reports are saved as CSV and HTML in the output folder, and logs are written to `logs/job_monitor.log`.

## Run (Web App)

Start the Flask web UI:

```powershell
python web_app.py
```

Open:

- `http://localhost:8000`

Enter LinkedIn credentials and search inputs in the form, then generate/download reports.

## Project Structure

- `main.py`: CLI entrypoint
- `web_app.py`: Flask UI
- `job_monitor/pipeline.py`: End-to-end workflow
- `job_monitor/providers/linkedin_content_provider.py`: LinkedIn login + content fetch
- `job_monitor/extractors/`: Content extraction logic
- `job_monitor/filters/`: Post filtering
- `job_monitor/storage/`: CSV/HTML report writing
- `templates/index.html`: Web form template

## Notes

- This is a basic automation tool that logs in to LinkedIn, searches by role/location, extracts matching content, and generates CSV/HTML reports for easy review.
- It is useful compared to manually using the LinkedIn app because it reduces repeated search effort, produces exportable structured data, and makes monitoring opportunities consistent across runs.
