from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class JobBoard(ABC):
    def __init__(self, driver: Optional[webdriver.Chrome] = None):
        self.driver = driver or self._setup_driver()
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up the Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set user agent to appear more human-like
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        return driver
    
    @abstractmethod
    async def login(self, email: str, password: str) -> bool:
        """Login to the job board"""
        pass
    
    @abstractmethod
    async def search_jobs(self, keywords: str, location: str) -> List[Dict[str, Any]]:
        """Search for jobs with the given criteria"""
        pass
    
    @abstractmethod
    async def apply_to_job(self, job_id: str, resume_path: str, cover_letter_path: Optional[str] = None) -> bool:
        """Apply to a specific job"""
        pass
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit() 