# Student Scores API

A FastAPI service for managing subjects, assessments, and student scores, with
validated JSON, Basic Authentication, and clear error responses.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
```

## Running

```powershell
uvicorn app.main:app --reload
```

- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json
- Default credentials (for write requests): username `admin`, password `changeme123`

## Running tests

```powershell
pytest
```

## Postman collection

Import `postman/student_scores_api.postman_collection.json` into Postman. It
contains a request for every endpoint, with Basic Auth pre-configured on the
write requests and `baseUrl` / `username` / `password` collection variables.

## Project structure

| Path | Purpose |
|------|---------|
| `app/main.py` | FastAPI app, router registration, exception handlers |
| `app/auth.py` | HTTP Basic auth dependency |
| `app/storage.py` | In-memory data store and ID generators |
| `app/models.py` | Pydantic request/response schemas |
| `app/routers/subjects.py` | Subject endpoints |
| `app/routers/assessments.py` | Assessment endpoints |
| `app/routers/scores.py` | Score endpoints, results, and averages |
| `tests/test_api.py` | API tests (pytest + FastAPI TestClient) |
| `postman/` | Postman collection |
| `samples/` | Real request/response examples |
| `docs/API.md` | Full endpoint reference |
| `AUTH_AND_VALIDATION.md` | How auth, validation, and errors protect student data |
| `pytest.ini` | Pytest configuration (adds project root to `sys.path`) |

```
student-scores-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── storage.py
│   ├── models.py
│   └── routers/
│       ├── __init__.py
│       ├── subjects.py
│       ├── assessments.py
│       └── scores.py
├── tests/
│   └── test_api.py
├── postman/
│   └── student_scores_api.postman_collection.json
├── samples/
│   └── sample_requests_responses.md
├── docs/
│   └── API.md
├── AUTH_AND_VALIDATION.md
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

## Design notes and limitations

- **Storage is in-memory** (Python dictionaries). There is no database, so all
  data resets when the server restarts. This is intentional for this brief, which
  concerns the API layer rather than persistence.
- **Authentication** is HTTP Basic. It sends credentials on every request, so it
  should only be used over HTTPS in a real deployment.
- **Error responses** all share one shape: `{"error": ..., "status_code": ...}`.

## Further documentation

- `docs/API.md` — full endpoint reference
- `samples/sample_requests_responses.md` — real request/response examples
- `AUTH_AND_VALIDATION.md` — how auth, validation, and error handling protect student data
