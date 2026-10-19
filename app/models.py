from pydantic import BaseModel, Field, field_validator


class Subject(BaseModel):
    subject_id: int
    name: str


class SubjectCreate(BaseModel):
    name: str = Field(min_length=1)


class Assessment(BaseModel):
    assessment_id: int
    subject_id: int
    name: str
    max_score: float


class AssessmentCreate(BaseModel):
    subject_id: int
    name: str = Field(min_length=1)
    max_score: float = Field(gt=0)


class Score(BaseModel):
    score_id: int
    student_name: str
    assessment_id: int
    value: float


class ScoreCreate(BaseModel):
    student_name: str = Field(min_length=1)
    assessment_id: int
    value: float = Field(ge=0)


class ScoreUpdate(BaseModel):
    value: float = Field(ge=0)