from fastapi import FastAPI, HTTPException
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


@app.get("/")
def root():
    return {"message": "Student Scores API is running. See /docs for documentation."}