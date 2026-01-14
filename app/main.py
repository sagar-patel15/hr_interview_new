from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from .core.database import connect_to_mongo, close_mongo_connection
from .api.endpoints import admin, interview, code_generator, auth, jobs, applicants, resume_parser_endpoint, results

app = FastAPI(title="AI Interview Backend", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        field = first_error.get("loc", [])[-1] if first_error.get("loc") else "field"
        msg = first_error.get("msg", "Validation error")
        
        if "missing" in first_error.get("type", ""):
            error_msg = f"{field} is required"
        elif "value_error" in first_error.get("type", ""):
            error_msg = msg.replace("Value error, ", "")
        else:
            error_msg = f"{field}: {msg}"
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": error_msg}
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Validation error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applicants.router, prefix="/api/jobs", tags=["applicants"])
app.include_router(resume_parser_endpoint.router, prefix="/api/resumes", tags=["resume-parser"])
app.include_router(results.router, prefix="/api/results", tags=["results"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(code_generator.router, prefix="/api/code", tags=["code-generator"])
app.include_router(interview.router, prefix="/api", tags=["interview"])

@app.get("/")
async def root():
    return {"message": "AI Interview Backend is running"}

app.mount("/", StaticFiles(directory="../", html=True), name="static")
