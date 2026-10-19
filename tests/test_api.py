from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH = ("admin", "changeme123")


def test_create_subject_requires_auth():
    response = client.post("/subjects/", json={"name": "Mathematics"})
    assert response.status_code == 401


def test_create_subject():
    response = client.post("/subjects/", json={"name": "Mathematics"}, auth=AUTH)
    assert response.status_code == 201
    assert response.json()["name"] == "Mathematics"


def test_create_assessment_unknown_subject():
    response = client.post(
        "/assessments/",
        json={"subject_id": 999, "name": "Midterm Exam", "max_score": 100},
        auth=AUTH,
    )
    assert response.status_code == 404


def test_add_score_exceeds_max():
    # assessment_id 1 (max_score 100) created here under subject 1
    client.post(
        "/assessments/",
        json={"subject_id": 1, "name": "Midterm Exam", "max_score": 100},
        auth=AUTH,
    )
    response = client.post(
        "/scores",
        json={"student_name": "Ada", "assessment_id": 1, "value": 150},
        auth=AUTH,
    )
    assert response.status_code == 400


def test_add_score_and_get_average():
    response = client.post(
        "/scores",
        json={"student_name": "Ada", "assessment_id": 1, "value": 80},
        auth=AUTH,
    )
    assert response.status_code == 201
    average = client.get("/students/Ada/average")
    assert average.status_code == 200
    assert average.json()["average"] == 80.0


def test_results_for_unknown_student():
    response = client.get("/students/Nobody/results")
    assert response.status_code == 404