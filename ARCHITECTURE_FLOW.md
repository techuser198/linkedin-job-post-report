# LinkedIn Job Monitor Architecture

## Overview

This app automates LinkedIn content search for job-related posts and generates downloadable reports.

- Input: LinkedIn credentials + role/location/days
- Processing: login, fetch HTML, extract posts, filter matches
- Output: timestamped CSV and HTML reports

## 1) End-to-End Flow

```mermaid
flowchart TD
    A[User opens Web UI] --> B[GET /]
    B --> C[index.html form]
    C --> D[POST /generate]
    D --> E{Input valid?}
    E -- No --> F[Render error]
    E -- Yes --> G[Build SearchCriteria]
    G --> H[run_pipeline]
    H --> I[Launch Playwright]
    I --> J[LinkedIn login]
    J --> K[Search content + scroll]
    K --> L[Get page HTML]
    L --> M[extract_posts]
    M --> N[filter_posts]
    N --> O[write_reports]
    O --> P[CSV + HTML in data/timestamp]
    P --> Q[Render success page]
    Q --> R[GET /download?file=...]
    R --> S[send_file attachment]
```

## 2) Component View

```mermaid
flowchart LR
    UI[templates/index.html]
    WEB[web_app.py\nRoutes: /, /generate, /download]
    DOMAIN[domain/models.py\nSearchCriteria, JobPost]
    PIPE[pipeline.py\nrun_pipeline]
    PROVIDER[providers/linkedin_content_provider.py]
    EXTRACT[extractors/linkedin_post_extractor.py]
    FILTER[filters/post_filters.py]
    STORE[storage/report_writer.py]
    OUT[(data/*.csv, data/*.html, logs/job_monitor.log)]

    UI --> WEB
    WEB --> DOMAIN
    WEB --> PIPE
    PIPE --> PROVIDER
    PIPE --> EXTRACT
    PIPE --> FILTER
    PIPE --> STORE
    STORE --> OUT
```

## 3) Runtime Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant F as Flask (web_app.py)
    participant P as Pipeline
    participant LI as LinkedIn (Playwright)
    participant X as Extractor/Filter
    participant W as Report Writer

    U->>B: Open app
    B->>F: GET /
    F-->>B: Return HTML form

    U->>B: Submit credentials + role/location/days
    B->>F: POST /generate
    F->>P: run_pipeline(criteria, creds)
    P->>LI: Login + search + fetch HTML
    LI-->>P: HTML content
    P->>X: Extract + filter posts
    X-->>P: Filtered posts
    P->>W: Write CSV + HTML
    W-->>P: File paths
    P-->>F: csv_path, html_path
    F-->>B: Success page with download links
```

## 4) Scope Notes

- Current source is LinkedIn content posts search (not LinkedIn Jobs listings API).
- Credentials from the form are used per request and not intentionally persisted by app code.
- Reports are generated with timestamps for each run.
