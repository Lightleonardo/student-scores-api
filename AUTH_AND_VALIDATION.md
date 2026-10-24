# Authentication, Validation, and Error Handling

## Authentication

Every endpoint that creates or modifies data requires HTTP Basic Authentication
(`app/auth.py`). Without it, anyone who can reach the service could add subjects,
attach assessments, or alter a student's score, and a single forged `PUT /scores`
would silently change a grade. Requiring credentials on writes closes that hole
while leaving read-only endpoints public, since subject and assessment names are
not sensitive.

Basic Auth is simple, but it sends the username and password with every request,
base64-encoded, which is not encryption. Over plain HTTP those credentials are
recoverable by anyone on the network path. **In any real deployment this API must
be served over HTTPS only; it must never be exposed over plain HTTP.** The
comparison in `verify_credentials` uses `secrets.compare_digest` rather than `==`
so that response time does not reveal how many leading characters of a guessed
password were correct.

## Validation

Validation happens in two layers.

**Pydantic** (`app/models.py`) rejects malformed requests before any endpoint
code runs. A missing `name`, a `value` that is not a number, or a `max_score` of
zero never reach the storage layer, so bad data cannot be written or later
averaged. This is automatic and returns `422`.

**Business rules** cover what Pydantic cannot express. A score of 150 is a valid
number in the abstract, but it is meaningless against an assessment whose
`max_score` is 100 — and Pydantic validates a score in isolation, without
knowledge of the assessment it references. That check therefore lives in the
endpoint (`app/routers/scores.py`), where both records are available, and returns
`400`.

## Clear error responses

A generic `500` tells a legitimate client nothing and looks like a broken
service. A specific `404` such as `"Subject 5 not found"` tells them exactly what
went wrong. Critically, these messages describe the request without exposing
internals — no stack traces, file paths, or database details that an attacker
could use to map the system. All errors share one shape,
`{"error": ..., "status_code": ...}`, so clients can handle failures uniformly.

## Why this matters for student records

Academic results are sensitive personal data. An unauthenticated write endpoint
would let anyone raise or lower a grade. A missing validation check would let a
corrupted score quietly distort an average that a school, a parent, or a
university relies on. Authentication, layered validation, and precise errors
together ensure that only trusted callers can change scores, and only
well-formed, logically valid values ever reach a student's record.
