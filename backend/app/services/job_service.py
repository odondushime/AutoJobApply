from app.schemas.job import JobSearchParams, JobResponse
from app.core.config import settings
from app.job_boards.linkedin import LinkedInJobBoard
import logging
from typing import Dict, Type
from .base import JobBoard

logger = logging.getLogger(__name__)

class JobService:
    def __init__(self):
        self.job_boards: Dict[str, Type[JobBoard]] = {
            "linkedin": LinkedInJobBoard,
            # Add other job boards here as they are implemented
        }
        self.active_boards: Dict[str, JobBoard] = {}
    
    def _get_job_board(self, board_name: str) -> JobBoard:
        """Get or create a job board instance"""
        if board_name not in self.active_boards:
            board_class = self.job_boards.get(board_name)
            if not board_class:
                raise ValueError(f"Unsupported job board: {board_name}")
            self.active_boards[board_name] = board_class()
        return self.active_boards[board_name]
    
    async def search_jobs(self, params: JobSearchParams) -> list[JobResponse]:
        """Search for jobs using the specified parameters"""
        try:
            board = self._get_job_board(params.job_board)
            
            # Get credentials from settings
            email = settings.LINKEDIN_EMAIL
            password = settings.LINKEDIN_PASSWORD
            
            if not email or not password:
                raise ValueError("Job board credentials not configured")
            
            # Login to the job board
            if not await board.login(email, password):
                raise Exception(f"Failed to login to {params.job_board}")
            
            # Search for jobs
            jobs = await board.search_jobs(params.keywords, params.location)
            
            # Convert to JobResponse objects
            return [JobResponse(**job) for job in jobs]
            
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            raise
    
    async def apply_to_job(self, job_id: str) -> bool:
        """Apply to a specific job"""
        try:
            # For now, we only support LinkedIn
            board = self._get_job_board("linkedin")
            
            # Get resume and cover letter paths from settings
            resume_path = settings.RESUME_PATH
            cover_letter_path = settings.COVER_LETTER_PATH
            
            if not resume_path:
                raise ValueError("Resume path not configured")
            
            # Apply to the job
            return await board.apply_to_job(job_id, resume_path, cover_letter_path)
            
        except Exception as e:
            logger.error(f"Error applying to job: {str(e)}")
            raise
    
    def cleanup(self):
        """Clean up job board instances"""
        for board in self.active_boards.values():
            board.close()
        self.active_boards.clear() 