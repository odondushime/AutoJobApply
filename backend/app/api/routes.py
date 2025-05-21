from fastapi import APIRouter, HTTPException
from app.schemas.job import JobSearchParams, JobResponse
from app.schemas.settings import Settings, SettingsUpdate
from app.services.job_service import JobService
from app.services.settings_service import SettingsService

router = APIRouter()
job_service = JobService()
settings_service = SettingsService()

@router.post("/jobs/search")
async def search_jobs(params: JobSearchParams) -> list[JobResponse]:
    """Search for jobs based on the provided parameters"""
    try:
        jobs = await job_service.search_jobs(params)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jobs/apply/{job_id}")
async def apply_to_job(job_id: str):
    """Apply to a specific job"""
    try:
        success = await job_service.apply_to_job(job_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to apply to job")
        return {"message": "Successfully applied to job"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings")
async def get_settings() -> Settings:
    """Get current application settings"""
    try:
        return await settings_service.get_settings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings")
async def update_settings(settings: SettingsUpdate) -> Settings:
    """Update application settings"""
    try:
        return await settings_service.update_settings(settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 