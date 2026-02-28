# Job Monitor Architecture and Flow (Text Diagram)

This version is pure text/ASCII so it displays correctly in any editor.

## 1) End-to-End Runtime Flow

+-------------------+
| User opens web UI |
+-------------------+
          |
          v
+------------------------------+
| GET /                        |
| web_app.py -> index.html     |
+------------------------------+
          |
          v
+--------------------------------------------+
| User submits form                          |
| linkedin_email, linkedin_password,         |
| role, location, days                       |
+--------------------------------------------+
          |
          v
+------------------------------+
| POST /generate               |
| Validate role/days input     |
+------------------------------+
      |                  |
      | invalid          | valid
      v                  v
+-------------------+  +-----------------------------------+
| Render error page |  | Build SearchCriteria              |
+-------------------+  | role/location/days                |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | run_pipeline(...)                 |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | Playwright launch                 |
                       | LinkedIn login                    |
                       | LinkedIn content search           |
                       | Scroll + capture HTML             |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | extract_posts(html, criteria)     |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | filter_posts(posts, criteria)     |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | write_reports(...)                |
                       | -> data/<timestamp>/report_*.csv  |
                       | -> data/<timestamp>/report_*.html |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | Render success page with links    |
                       +-----------------------------------+
                                      |
                                      v
                       +-----------------------------------+
                       | GET /download?file=...            |
                       | send_file(...)                    |
                       +-----------------------------------+


## 2) Layered Component Diagram

+---------------------- Web Layer ----------------------+
| templates/index.html                                 |
| web_app.py (/, /generate, /download)                |
+------------------------------------------------------+
                         |
                         v
+-------------------- Domain Layer ---------------------+
| SearchCriteria                                         |
| JobPost                                                |
+-------------------------------------------------------+
                         |
                         v
+------------------- Pipeline Layer --------------------+
| pipeline.py : run_pipeline                             |
+-------------------------------------------------------+
                         |
                         v
+------------------- Provider Layer --------------------+
| linkedin_content_provider.py                           |
| - login(page, email, password)                         |
| - fetch_posts_html(page, criteria)                     |
+-------------------------------------------------------+
                         |
                         v
+------------------ Processing Layer -------------------+
| linkedin_post_extractor.py : extract_posts             |
| post_filters.py            : filter_posts              |
+-------------------------------------------------------+
                         |
                         v
+-------------------- Storage Layer --------------------+
| report_writer.py : write_reports                       |
+-------------------------------------------------------+
                         |
                         v
+----------------------- Outputs -----------------------+
| data/<timestamp>/report_*.csv                          |
| data/<timestamp>/report_*.html                         |
| logs/job_monitor.log                                   |
+-------------------------------------------------------+


## 3) Sequence View (Text)

User
  -> Browser: open site
Browser
  -> Flask(web_app.py): GET /
Flask
  -> Browser: return HTML form

User
  -> Browser: submit credentials + role/location/days
Browser
  -> Flask(web_app.py): POST /generate
Flask
  -> Pipeline(run_pipeline): start job
Pipeline
  -> LinkedIn via Playwright: login + search + fetch HTML
LinkedIn/Playwright
  -> Pipeline: HTML content
Pipeline
  -> Extractor/Filter: parse + filter
Extractor/Filter
  -> Pipeline: filtered JobPost list
Pipeline
  -> ReportWriter: write CSV/HTML
ReportWriter
  -> Pipeline: file paths
Pipeline
  -> Flask: success + links
Flask
  -> Browser: response page
Browser
  -> Flask: GET /download?file=...
Flask
  -> Browser: file attachment


## 4) Important Scope Note

- Current source is LinkedIn content posts search, not LinkedIn Jobs listings search.
- Credentials from form are used in-memory per request and not intentionally persisted by app code.
- Reports are generated as timestamped CSV and HTML files.
