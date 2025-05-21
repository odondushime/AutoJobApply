import os
import logging
from pathlib import Path
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class JobBoardBase(ABC):
    """Base class for job board implementations"""
    
    def __init__(self, config):
        self.config = config
        self.driver = self._setup_webdriver()
        self.credentials = self._get_credentials()
        self.personal_info = config.get('personal_info', {})
        
        # Set default paths if not specified
        self.resume_path = Path(config.get('resume_path', 'resumes/resume.pdf'))
        self.cover_letter_path = Path(config.get('cover_letter_path', 'cover_letters/cover_letter.pdf'))
        
        # Check if cover letter exists and warn if not
        if not self.cover_letter_path.exists():
            logger.warning(f"Cover letter not found at {self.cover_letter_path}")
        
        # Check if resume exists and warn if not
        if not self.resume_path.exists():
            logger.warning(f"Resume not found at {self.resume_path}")
    
    def _setup_webdriver(self):
        """Set up and configure Chrome WebDriver"""
        chrome_options = Options()
        
        if self.config.get("headless", False):
            chrome_options.add_argument("--headless")
            
        # Use existing Chrome profile
        if self.config.get("browser_settings", {}).get("use_existing_profile", False):
            chrome_profile_path = str(Path(self.config["browser_settings"]["chrome_profile_path"]).expanduser().resolve())
            chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
            chrome_options.add_argument("--profile-directory=Default")
            
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    
    def _get_credentials(self):
        """Get credentials for the job board"""
        board_name = self.board_name
        if board_name not in self.config["job_boards"]:
            raise ValueError(f"Job board {board_name} not found in config")
        return self.config["job_boards"][board_name]["credentials"]
    
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
    def apply_to_job(self, job):
        """Apply to a specific job"""
        pass
    
    def quit(self):
        """Close the browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def get_credentials(self, platform):
        """Safely get credentials for a specific platform.
        
        Args:
            platform (str): The platform name (e.g., 'linkedin', 'indeed')
            
        Returns:
            dict: A dictionary with 'username' and 'password' keys
        """
        platform_creds = self.credentials.get(platform, {})
        
        # If credentials for this platform don't exist, return empty dict with None values
        if not platform_creds:
            logger.warning(f"No credentials found for {platform}")
            return {"username": None, "password": None}
        
        return {
            "username": platform_creds.get("username"),
            "password": platform_creds.get("password")
        }
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add a random delay to simulate human behavior
        
        Args:
            min_seconds (float): Minimum delay in seconds
            max_seconds (float): Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def wait_for_element(self, by, value, timeout=10, condition="presence"):
        """Wait for an element to be present/visible/clickable
        
        Args:
            by: Selenium By locator strategy
            value: The locator value
            timeout (int): Maximum wait time in seconds
            condition (str): One of 'presence', 'visibility', 'clickable'
            
        Returns:
            WebElement: The found element
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        if not self.driver:
            raise ValueError("WebDriver not initialized")
            
        wait = WebDriverWait(self.driver, timeout)
        
        if condition == "presence":
            return wait.until(EC.presence_of_element_located((by, value)))
        elif condition == "visibility":
            return wait.until(EC.visibility_of_element_located((by, value)))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable((by, value)))
        else:
            raise ValueError(f"Unknown condition: {condition}")