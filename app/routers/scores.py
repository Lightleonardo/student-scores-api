from fastapi import APIRouter, Depends, HTTPException
from app import storage
from app.auth import verify_credentials
from app.models import Score, ScoreCreate, ScoreUpdate

router = APIRouter(tags=["scores"])


@router.post("/scores", response_model=Score, status_code=201)
def add_score(payload: ScoreCreate, username: str = Depends(verify_credentials)):
    assessment = storage.assessments.get(payload.assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if payload.value > assessment["max_score"]:
        raise HTTPException(
            status_code=400,
            detail=f"Score {payload.value} exceeds max_score {assessment['max_score']}",
        )
    score_id = storage.next_score_id()
    score = {
        "score_id": score_id,
        "student_name": payload.student_name,
        "assessment_id": payload.assessment_id,
        "value": payload.value,
    }
    storage.scores[score_id] = score
    return score


@router.put("/scores/{score_id}", response_model=Score)
def update_score(score_id: int, payload: ScoreUpdate, username: str = Depends(verify_credentials)):
    score = storage.scores.get(score_id)
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    assessment = storage.assessments[score["assessment_id"]]
    if payload.value > assessment["max_score"]:
        raise HTTPException(status_code=400, detail="Score exceeds max_score")
    score["value"] = payload.value
    return score


@router.get("/students/{student_name}/results", response_model=list[Score])
def get_student_results(student_name: str):
    results = [s for s in storage.scores.values() if s["student_name"] == student_name]
    if not results:
        raise HTTPException(status_code=404, detail=f"No results found for {student_name}")
    return results


@router.get("/students/{student_name}/average")
def get_student_average(student_name: str):
    results = [s for s in storage.scores.values() if s["student_name"] == student_name]
    if not results:
        raise HTTPException(status_code=404, detail=f"No results found for {student_name}")
    average = sum(r["value"] for r in results) / len(results)
    return {"student_name": student_name, "average": round(average, 2)}