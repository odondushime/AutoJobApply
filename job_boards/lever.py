"""
Lever job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class LeverBoard(JobBoardBase):
    """Lever job board implementation"""
    
    @property
    def board_name(self):
        return "lever"
    
    def login(self):
        """Login to Lever"""
        # Lever doesn't require login for job searching
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Lever"""
        jobs = []
        try:
            # Build search URL - Lever uses company-specific URLs
            search_url = "https://jobs.lever.co/sales"
            self.driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.posting")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h5.posting-title")
                    company_elem = job.find_element(By.CSS_SELECTOR, "span.posting-company")
                    location_elem = job.find_element(By.CSS_SELECTOR, "span.posting-location")
                    link_elem = job.find_element(By.CSS_SELECTOR, "a.posting-title")
                    
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
                    logger.error(f"Error parsing Lever job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching Lever jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Lever"""
        try:
            self.driver.get(job_data["url"])
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button.postings-btn"
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
                logger.warning("Could not find expected form elements on Lever")
                return False
                
        except Exception as e:
            logger.error(f"Error during Lever application: {e}")
            return False 