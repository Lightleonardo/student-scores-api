from fastapi import APIRouter, Depends, HTTPException
from app import storage
from app.auth import verify_credentials
from app.models import Subject, SubjectCreate

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("/", response_model=Subject, status_code=201)
def create_subject(payload: SubjectCreate, username: str = Depends(verify_credentials)):
    subject_id = storage.next_subject_id()
    subject = {"subject_id": subject_id, "name": payload.name}
    storage.subjects[subject_id] = subject
    return subject


@router.get("/", response_model=list[Subject])
def list_subjects():
    return list(storage.subjects.values())


@router.get("/{subject_id}", response_model=Subject)
def get_subject(subject_id: int):
    subject = storage.subjects.get(subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    return subject