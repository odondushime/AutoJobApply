from pydantic import BaseModel
from typing import Optional

class JobSearchParams(BaseModel):
    keywords: str
    location: str
    job_board: str

class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    job_board: str
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    requirements: Optional[list[str]] = None 