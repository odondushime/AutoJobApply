"""
Greenhouse job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class GreenhouseBoard(JobBoardBase):
    """Greenhouse job board implementation"""
    
    @property
    def board_name(self):
        return "greenhouse"
    
    def login(self):
        """Login to Greenhouse"""
        # Greenhouse doesn't require login for job searching
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Greenhouse"""
        jobs = []
        try:
            # Build search URL - Greenhouse uses company-specific URLs
            search_url = "https://boards.greenhouse.io/sales"
            self.driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.opening")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "a.opening-title")
                    location_elem = job.find_element(By.CSS_SELECTOR, "span.location")
                    
                    job_data = {
                        "job_title": title_elem.text.strip(),
                        "company": "Company Name",  # Greenhouse doesn't show company name in listing
                        "location": location_elem.text.strip(),
                        "url": title_elem.get_attribute("href"),
                        "job_board": self.board_name
                    }
                    job_data["job_id"] = self._get_unique_job_id(job_data)
                    jobs.append(job_data)
                    
                except NoSuchElementException:
                    continue
                except Exception as e:
                    logger.error(f"Error parsing Greenhouse job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching Greenhouse jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Greenhouse"""
        try:
            self.driver.get(job_data["url"])
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button#apply_button"
            )
            if not apply_button:
                return False
            apply_button.click()
            
            # Wait for application form
            time.sleep(2)
            
            # Fill out application form
            try:
                # Fill name if required
                name_field = self._wait_for_element(By.CSS_SELECTOR, "input#first_name")
                if name_field:
                    name_field.send_keys("Your Name")
                
                # Fill email if required
                email_field = self._wait_for_element(By.CSS_SELECTOR, "input#email")
                if email_field:
                    email_field.send_keys(self.credentials.get("email", ""))
                
                # Upload resume if required
                resume_upload = self._wait_for_element(By.CSS_SELECTOR, "input#resume")
                if resume_upload:
                    resume_upload.send_keys(str(self.resume_path.absolute()))
                
                # Submit application
                submit_button = self._wait_for_clickable(By.CSS_SELECTOR, "input#submit_app")
                if submit_button:
                    submit_button.click()
                    time.sleep(3)
                    return True
                
            except NoSuchElementException:
                logger.warning("Could not find expected form elements on Greenhouse")
                return False
                
        except Exception as e:
            logger.error(f"Error during Greenhouse application: {e}")
            return False 