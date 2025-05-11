"""
BuiltIn job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class BuiltInBoard(JobBoardBase):
    """BuiltIn job board implementation"""
    
    @property
    def board_name(self):
        return "builtin"
    
    def login(self):
        """Login to BuiltIn"""
        # BuiltIn doesn't require login for job searching
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs on BuiltIn"""
        jobs = []
        try:
            # Process keywords for URL
            keyword_str = "developer"  # Default fallback
            if isinstance(keywords, list) and keywords:
                # Try to use the first keyword that's developer-related
                dev_keywords = ["developer", "engineer", "software", "coding", "programmer"]
                for kw in keywords:
                    if any(dev in kw.lower() for dev in dev_keywords):
                        keyword_str = kw.replace(" ", "-").lower()
                        break
            
            # Process location for URL
            location_str = ""
            if location and location.lower() != "remote":
                location_parts = location.split(",")
                if len(location_parts) > 0:
                    city = location_parts[0].strip().replace(" ", "-").lower()
                    location_str = f"/{city}"
            
            # Build search URL
            search_url = f"https://builtin.com/jobs{location_str}/{keyword_str}"
            logger.info(f"Searching BuiltIn with URL: {search_url}")
            self.driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h2.job-title")
                    company_elem = job.find_element(By.CSS_SELECTOR, "div.company-name")
                    location_elem = job.find_element(By.CSS_SELECTOR, "div.location")
                    link_elem = job.find_element(By.CSS_SELECTOR, "a.job-link")
                    
                    job_data = {
                        "job_title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip(),
                        "url": link_elem.get_attribute("href"),
                        "job_board": self.board_name
                    }
                    job_data["job_id"] = self._get_unique_job_id(job_data)
                    jobs.append(job_data)
                    
                except NoSuchElementException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing BuiltIn job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching BuiltIn jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on BuiltIn"""
        try:
            self.driver.get(job_data["url"])
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button.apply-button"
            )
            if not apply_button:
                return False
            apply_button.click()
            
            # Wait for application form
            time.sleep(2)
            
            # Fill out application form
            try:
                # Fill name if required
                name_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='name']")
                if name_field:
                    name_field.send_keys(self.config.get("personal_info", {}).get("name", ""))
                
                # Fill email if required
                email_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='email']")
                if email_field:
                    email_field.send_keys(self.credentials.get("email", ""))
                
                # Upload resume if required
                resume_upload = self._wait_for_element(By.CSS_SELECTOR, "input[type='file']")
                if resume_upload:
                    resume_upload.send_keys(str(self.resume_path.absolute()))
                
                # Submit application
                submit_button = self._wait_for_clickable(By.CSS_SELECTOR, "button[type='submit']")
                if submit_button:
                    submit_button.click()
                    time.sleep(3)
                    return True
                
            except NoSuchElementException:
                logger.warning("Could not find expected form elements on BuiltIn")
                return False
                
        except Exception as e:
            logger.error(f"Error during BuiltIn application: {e}")
            return False

    def _safe_click(self, element, timeout=3):
        """Safely click an element with retry logic"""
        if not element:
            return False
        
        max_retries = 3
        for i in range(max_retries):
            try:
                element.click()
                return True
            except Exception as e:
                if i == max_retries - 1:
                    logger.error(f"Failed to click element after {max_retries} tries: {e}")
                    return False
                time.sleep(1) 