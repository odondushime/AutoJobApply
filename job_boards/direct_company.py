"""
Direct company job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class DirectCompanyBoard(JobBoardBase):
    """Direct company job board implementation"""
    
    @property
    def board_name(self):
        return "direct_company"
    
    def login(self):
        """No login required for direct company applications"""
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs on direct company websites"""
        jobs = []
        try:
            # List of company career URLs
            company_urls = [
                "https://careers.google.com/",
                "https://www.amazon.jobs/",
                "https://careers.microsoft.com/",
                "https://careers.jpmorgan.com/",
                "https://stripe.com/jobs",
                "https://about.gitlab.com/jobs/",
                "https://automattic.com/work-with-us/",
                "https://zapier.com/jobs",
                "https://jobs.cvshealth.com/",
                "https://delta.avature.net/careers"
            ]
            
            for url in company_urls:
                self.driver.get(url)
                time.sleep(3)  # Wait for page to load
                
                # Example: Find job listings on the page
                # This is a placeholder and should be customized for each company's website
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
                        logger.error(f"Error parsing job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on direct company websites"""
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
                    name_field.send_keys(self.config["personal_info"]["name"])
                
                # Fill email if required
                email_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='email']")
                if email_field:
                    email_field.send_keys(self.config["personal_info"]["email"])
                
                # Fill phone if required
                phone_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='phone']")
                if phone_field:
                    phone_field.send_keys(self.config["personal_info"]["phone"])
                
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
                logger.warning("Could not find expected form elements")
                return False
                
        except Exception as e:
            logger.error(f"Error during application: {e}")
            return False 