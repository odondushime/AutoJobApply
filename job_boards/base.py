"""
Base class for job board scrapers and applications
"""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class JobBoardBase(ABC):
    """Base class for all job board implementations"""
    
    def __init__(self, config, driver=None):
        self.config = config
        self.driver = driver
        self.resume_path = Path(config.get("resume_path", "resume.pdf"))
        self.cover_letter_path = Path(config.get("cover_letter_path", "cover_letter.pdf"))
        self.credentials = config.get("credentials", {}).get(self.board_name, {})
        
        # Verify paths exist
        if not self.resume_path.exists():
            logger.warning(f"Resume not found at {self.resume_path}")
        if not self.cover_letter_path.exists():
            logger.warning(f"Cover letter not found at {self.cover_letter_path}")
    
    @property
    @abstractmethod
    def board_name(self):
        """Return the name of the job board"""
        pass
    
    @abstractmethod
    def login(self):
        """Login to the job board"""
        pass
    
    @abstractmethod
    def search_jobs(self, keywords, location):
        """Search for jobs on the board"""
        pass
    
    @abstractmethod
    def apply_to_job(self, job_data):
        """Apply to a specific job"""
        pass
    
    def _get_unique_job_id(self, job_data):
        """Generate a unique job ID for tracking"""
        base_id = f"{self.board_name}_{job_data['company']}_{job_data['job_title']}"
        return "".join(c for c in base_id if c.isalnum()).lower()
    
    def _wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {value}")
            return None
    
    def _wait_for_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for clickable element: {value}")
            return None 