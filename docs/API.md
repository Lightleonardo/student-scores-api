# Student Scores API — Endpoint Reference

Base URL (local): `http://127.0.0.1:8000`

This is a written reference for reading the repo without running the server. The
running app also exposes auto-generated interactive docs (Swagger UI) at `/docs`
and the OpenAPI schema at `/openapi.json`.

## Authentication

Write endpoints (`POST`, `PUT`) require **HTTP Basic Authentication**.

| Username | Password |
|----------|----------|
| `admin`  | `changeme123` |

Read endpoints (`GET`) are public. A request to a protected endpoint without
valid credentials returns `401 Unauthorized` with a `WWW-Authenticate: Basic`
header.

## Error response shape

Every error uses the same JSON shape:

```json
{"error": "<message or list of validation errors>", "status_code": <code>}
```

| Code | Meaning in this API |
|------|---------------------|
| `200` | Successful `GET` |
| `201` | Successful `POST` that created a resource |
| `400` | Valid JSON, but a business rule failed (score exceeds `max_score`) |
| `401` | Missing or invalid Basic Auth credentials |
| `404` | A referenced ID (subject, assessment, score) or student has no results |
| `422` | Request body failed Pydantic validation (wrong type, missing/out-of-range field) |

## Resources

### Subject

```json
{
  "subject_id": 1,
  "name": "Mathematics"
}
```

### Assessment

```json
{
  "assessment_id": 1,
  "subject_id": 1,
  "name": "Midterm Exam",
  "max_score": 100.0
}
```

### Score

```json
{
  "score_id": 1,
  "student_name": "Ada Lovelace",
  "assessment_id": 1,
  "value": 95.0
}
```

## Endpoint summary

| Method | Path | Auth | Request body | Response | Error codes |
|--------|------|------|--------------|----------|-------------|
| GET | `/` | No | — | `{"message": "..."}` | — |
| POST | `/subjects/` | Yes | `SubjectCreate` | `Subject` | 401, 422 |
| GET | `/subjects/` | No | — | `list[Subject]` | — |
| GET | `/subjects/{subject_id}` | No | — | `Subject` | 404, 422 |
| POST | `/assessments/` | Yes | `AssessmentCreate` | `Assessment` | 401, 404, 422 |
| GET | `/assessments/` | No | — | `list[Assessment]` | — |
| GET | `/assessments/{assessment_id}` | No | — | `Assessment` | 404, 422 |
| POST | `/scores` | Yes | `ScoreCreate` | `Score` | 401, 404, 400, 422 |
| PUT | `/scores/{score_id}` | Yes | `ScoreUpdate` | `Score` | 401, 404, 400, 422 |
| GET | `/students/{student_name}/results` | No | — | `list[Score]` | 404 |
| GET | `/students/{student_name}/average` | No | — | `{"student_name": ..., "average": ...}` | 404 |

## Request body schemas

### SubjectCreate — `POST /subjects/`

| Field | Type | Rules |
|-------|------|-------|
| `name` | string | required, min length 1 |

### AssessmentCreate — `POST /assessments/`

| Field | Type | Rules |
|-------|------|-------|
| `subject_id` | integer | required; must reference an existing subject |
| `name` | string | required, min length 1 |
| `max_score` | number | required, greater than 0 |

### ScoreCreate — `POST /scores`

| Field | Type | Rules |
|-------|------|-------|
| `student_name` | string | required, min length 1 |
| `assessment_id` | integer | required; must reference an existing assessment |
| `value` | number | required, greater than or equal to 0; must not exceed the assessment's `max_score` |

### ScoreUpdate — `PUT /scores/{score_id}`

| Field | Type | Rules |
|-------|------|-------|
| `value` | number | required, greater than or equal to 0; must not exceed the assessment's `max_score` |

## Endpoint details

### GET /

Health check / entry point.

**Response `200`**

```json
{"message": "Student Scores API is running. See /docs for documentation."}
```

### POST /subjects/

Create a subject. **Auth required.**

**Request**

```json
{"name": "Mathematics"}
```

**Response `201`**

```json
{"subject_id": 1, "name": "Mathematics"}
```

**Errors** — `401` missing/invalid credentials; `422` body validation failed.

### GET /subjects/

List all subjects. **Public.**

**Response `200`**

```json
[{"subject_id": 1, "name": "Mathematics"}]
```

### GET /subjects/{subject_id}

Get a single subject. **Public.**

**Response `200`**

```json
{"subject_id": 1, "name": "Mathematics"}
```

**Errors** — `404` subject not found; `422` `subject_id` is not an integer.

### POST /assessments/

Create an assessment under a subject. **Auth required.**

**Request**

```json
{"subject_id": 1, "name": "Midterm Exam", "max_score": 100}
```

**Response `201`**

```json
{"assessment_id": 1, "subject_id": 1, "name": "Midterm Exam", "max_score": 100.0}
```

**Errors** — `401` missing/invalid credentials; `404` referenced subject does not
exist; `422` body validation failed (e.g. `max_score` ≤ 0).

### GET /assessments/

List all assessments. **Public.**

**Response `200`**

```json
[{"assessment_id": 1, "subject_id": 1, "name": "Midterm Exam", "max_score": 100.0}]
```

### GET /assessments/{assessment_id}

Get a single assessment. **Public.**

**Response `200`**

```json
{"assessment_id": 1, "subject_id": 1, "name": "Midterm Exam", "max_score": 100.0}
```

**Errors** — `404` assessment not found; `422` `assessment_id` is not an integer.

### POST /scores

Add a score for a student on an assessment. **Auth required.**

**Request**

```json
{"student_name": "Ada Lovelace", "assessment_id": 1, "value": 80}
```

**Response `201`**

```json
{"score_id": 1, "student_name": "Ada Lovelace", "assessment_id": 1, "value": 80.0}
```

**Errors** — `401` missing/invalid credentials; `404` assessment does not exist;
`400` `value` exceeds the assessment's `max_score`; `422` body validation failed.

### PUT /scores/{score_id}

Update an existing score. **Auth required.**

**Request**

```json
{"value": 95}
```

**Response `200`**

```json
{"score_id": 1, "student_name": "Ada Lovelace", "assessment_id": 1, "value": 95.0}
```

**Errors** — `401` missing/invalid credentials; `404` score does not exist;
`400` `value` exceeds the assessment's `max_score`; `422` body validation failed.

### GET /students/{student_name}/results

Get every score recorded for a student. **Public.**

**Response `200`**

```json
[{"score_id": 1, "student_name": "Ada Lovelace", "assessment_id": 1, "value": 95.0}]
```

**Errors** — `404` the student has no results.

### GET /students/{student_name}/average

Get the mean of all of a student's scores, rounded to 2 decimal places.
**Public.**

**Response `200`**

```json
{"student_name": "Ada Lovelace", "average": 95.0}
```

**Errors** — `404` the student has no results.
