"""
Hired job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class HiredBoard(JobBoardBase):
    """Hired job board implementation"""
    
    @property
    def board_name(self):
        return "hired"
    
    def login(self):
        """Login to Hired"""
        if not self.credentials.get("email") or not self.credentials.get("password"):
            logger.warning("No Hired credentials found")
            return False
        
        try:
            self.driver.get("https://hired.com/login")
            
            # Wait for and fill email
            email_field = self._wait_for_element(By.CSS_SELECTOR, "input[type='email']")
            if not email_field:
                return False
            email_field.send_keys(self.credentials["email"])
            
            # Wait for and fill password
            password_field = self._wait_for_element(By.CSS_SELECTOR, "input[type='password']")
            if not password_field:
                return False
            password_field.send_keys(self.credentials["password"])
            
            # Click sign in
            signin_button = self._wait_for_clickable(By.CSS_SELECTOR, "button[type='submit']")
            if not signin_button:
                return False
            signin_button.click()
            
            # Wait for successful login
            time.sleep(5)
            return "Sign Out" in self.driver.page_source
            
        except Exception as e:
            logger.error(f"Error logging in to Hired: {e}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Hired"""
        jobs = []
        try:
            # Build search URL
            search_url = "https://hired.com/jobs/sales"
            self.driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h3.job-title")
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
                    logger.error(f"Error parsing Hired job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching Hired jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Hired"""
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
                    name_field.send_keys("Your Name")
                
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
                logger.warning("Could not find expected form elements on Hired")
                return False
                
        except Exception as e:
            logger.error(f"Error during Hired application: {e}")
            return False 