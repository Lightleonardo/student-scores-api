from fastapi import APIRouter, Depends, HTTPException
from app import storage
from app.auth import verify_credentials
from app.models import Assessment, AssessmentCreate

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("/", response_model=Assessment, status_code=201)
def create_assessment(payload: AssessmentCreate, username: str = Depends(verify_credentials)):
    # Verify subject exists
    if payload.subject_id not in storage.subjects:
        raise HTTPException(status_code=404, detail="Subject not found")
    assessment_id = storage.next_assessment_id()
    assessment = {
        "assessment_id": assessment_id,
        "subject_id": payload.subject_id,
        "name": payload.name,
        "max_score": payload.max_score,
    }
    storage.assessments[assessment_id] = assessment
    return assessment


@router.get("/", response_model=list[Assessment])
def list_assessments():
    return list(storage.assessments.values())


@router.get("/{assessment_id}", response_model=Assessment)
def get_assessment(assessment_id: int):
    assessment = storage.assessments.get(assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail=f"Assessment {assessment_id} not found")
    return assessment