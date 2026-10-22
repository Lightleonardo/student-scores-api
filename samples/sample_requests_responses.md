# Sample Requests and Responses

Every example below was captured by calling the running server
(`uvicorn app.main:app --reload`) at `http://127.0.0.1:8000`. The responses are
verbatim, including status codes.

Basic Auth credentials used on write requests: `admin` / `changeme123`.

The examples follow a realistic flow: create a subject, create an assessment
under it, add a score, update it, then read the student's results and average.

---

## GET / — health check

**Request**

```
GET http://127.0.0.1:8000/
```

**Response** — `200 OK`

```json
{"message":"Student Scores API is running. See /docs for documentation."}
```

---

## POST /subjects/ — create a subject

### Without credentials

**Request**

```
POST http://127.0.0.1:8000/subjects/
Content-Type: application/json

{"name": "Mathematics"}
```

**Response** — `401 Unauthorized`

```json
{"error":"Not authenticated","status_code":401}
```

### With valid credentials

**Request**

```
POST http://127.0.0.1:8000/subjects/
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"name": "Mathematics"}
```

**Response** — `201 Created`

```json
{"subject_id":1,"name":"Mathematics"}
```

---

## GET /subjects/ — list subjects

**Request**

```
GET http://127.0.0.1:8000/subjects/
```

**Response** — `200 OK`

```json
[{"subject_id":1,"name":"Mathematics"}]
```

---

## GET /subjects/{subject_id} — get one subject

**Request**

```
GET http://127.0.0.1:8000/subjects/1
```

**Response** — `200 OK`

```json
{"subject_id":1,"name":"Mathematics"}
```

**Request (unknown ID)**

```
GET http://127.0.0.1:8000/subjects/999
```

**Response** — `404 Not Found`

```json
{"error":"Subject 999 not found","status_code":404}
```

---

## POST /assessments/ — create an assessment

### Referencing a subject that does not exist

**Request**

```
POST http://127.0.0.1:8000/assessments/
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"subject_id": 999, "name": "Midterm Exam", "max_score": 100}
```

**Response** — `404 Not Found`

```json
{"error":"Subject not found","status_code":404}
```

### Valid request

**Request**

```
POST http://127.0.0.1:8000/assessments/
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"subject_id": 1, "name": "Midterm Exam", "max_score": 100}
```

**Response** — `201 Created`

```json
{"assessment_id":1,"subject_id":1,"name":"Midterm Exam","max_score":100.0}
```

---

## GET /assessments/ — list assessments

**Request**

```
GET http://127.0.0.1:8000/assessments/
```

**Response** — `200 OK`

```json
[{"assessment_id":1,"subject_id":1,"name":"Midterm Exam","max_score":100.0}]
```

---

## GET /assessments/{assessment_id} — get one assessment

**Request**

```
GET http://127.0.0.1:8000/assessments/1
```

**Response** — `200 OK`

```json
{"assessment_id":1,"subject_id":1,"name":"Midterm Exam","max_score":100.0}
```

---

## POST /scores — add a score

### Value above the assessment's max_score

**Request**

```
POST http://127.0.0.1:8000/scores
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"student_name": "Ada Lovelace", "assessment_id": 1, "value": 150}
```

**Response** — `400 Bad Request`

```json
{"error":"Score 150.0 exceeds max_score 100.0","status_code":400}
```

### Valid request

**Request**

```
POST http://127.0.0.1:8000/scores
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"student_name": "Ada Lovelace", "assessment_id": 1, "value": 80}
```

**Response** — `201 Created`

```json
{"score_id":1,"student_name":"Ada Lovelace","assessment_id":1,"value":80.0}
```

---

## PUT /scores/{score_id} — update a score

**Request**

```
PUT http://127.0.0.1:8000/scores/1
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"value": 95}
```

**Response** — `200 OK`

```json
{"score_id":1,"student_name":"Ada Lovelace","assessment_id":1,"value":95.0}
```

**Request (unknown score ID)**

```
PUT http://127.0.0.1:8000/scores/999
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{"value": 50}
```

**Response** — `404 Not Found`

```json
{"error":"Score not found","status_code":404}
```

---

## GET /students/{student_name}/results — a student's results

**Request**

```
GET http://127.0.0.1:8000/students/Ada Lovelace/results
```

**Response** — `200 OK`

```json
[{"score_id":1,"student_name":"Ada Lovelace","assessment_id":1,"value":95.0}]
```

**Request (student with no scores)**

```
GET http://127.0.0.1:8000/students/Nobody/results
```

**Response** — `404 Not Found`

```json
{"error":"No results found for Nobody","status_code":404}
```

---

## GET /students/{student_name}/average — a student's average

**Request**

```
GET http://127.0.0.1:8000/students/Ada Lovelace/average
```

**Response** — `200 OK`

```json
{"student_name":"Ada Lovelace","average":95.0}
```

---

## POST /subjects/ — invalid body (422 shape)

**Request**

```
POST http://127.0.0.1:8000/subjects/
Authorization: Basic YWRtaW46Y2hhbmdlbWUxMjM=
Content-Type: application/json

{}
```

**Response** — `422 Unprocessable Entity`

```json
{"error":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":{}}],"status_code":422}
```

Note: this is the same `{"error": ..., "status_code": ...}` shape used by all
other errors. Pydantic validation failures raise `RequestValidationError`
rather than `HTTPException`, so the app registers a second exception handler
for them in `app/main.py`.
