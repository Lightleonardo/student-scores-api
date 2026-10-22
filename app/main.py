from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import subjects, assessments, scores

app = FastAPI(title="Student Scores API", version="1.0.0")

app.include_router(subjects.router)
app.include_router(assessments.router)
app.include_router(scores.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": jsonable_encoder(exc.errors()), "status_code": 422},
    )


@app.get("/")
def root():
    return {"message": "Student Scores API is running. See /docs for documentation."}