"""
Indeed job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class IndeedBoard(JobBoardBase):
    """Indeed job board implementation"""
    
    @property
    def board_name(self):
        return "indeed"
    
    def login(self):
        """Login to Indeed"""
        try:
            self.driver.get("https://www.indeed.com/account/login")
            time.sleep(2)
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Try to find and click the Google login button
            google_button = self._wait_for_clickable(
                By.CSS_SELECTOR,
                "button[data-tn-element='google-login-button']"
            )
            if google_button:
                google_button.click()
                time.sleep(2)
                
                # Handle Google login
                email_field = self._wait_for_element(
                    By.CSS_SELECTOR,
                    "input[type='email']"
                )
                if email_field:
                    email_field.send_keys(self.credentials.get("email", ""))
                    next_button = self._wait_for_clickable(
                        By.CSS_SELECTOR,
                        "button[type='submit']"
                    )
                    if next_button:
                        next_button.click()
                        time.sleep(2)
                        
                        # Wait for password field
                        password_field = self._wait_for_element(
                            By.CSS_SELECTOR,
                            "input[type='password']"
                        )
                        if password_field:
                            password_field.send_keys(self.credentials.get("password", ""))
                            submit_button = self._wait_for_clickable(
                                By.CSS_SELECTOR,
                                "button[type='submit']"
                            )
                            if submit_button:
                                submit_button.click()
                                time.sleep(3)
                                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error during Indeed login: {e}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Indeed"""
        jobs = []
        try:
            # Format keywords for URL
            if isinstance(keywords, list):
                keyword_str = "+".join(keywords)
            else:
                keyword_str = keywords
                
            # Format location for URL
            location_str = location.replace(" ", "+") if location else "remote"
            
            # Build search URL
            search_url = f"https://www.indeed.com/jobs?q={keyword_str}&l={location_str}"
            logger.info(f"Searching Indeed with URL: {search_url}")
            self.driver.get(search_url)
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return jobs
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h2.jobTitle")
                    company_elem = job.find_element(By.CSS_SELECTOR, "span.companyName")
                    location_elem = job.find_element(By.CSS_SELECTOR, "div.companyLocation")
                    link_elem = job.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle")
                    
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
                    logger.error(f"Error parsing Indeed job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching Indeed jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Indeed"""
        try:
            self.driver.get(job_data["url"])
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button[data-testid='apply-button']"
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
                    name_field.send_keys(self._get_config_value("personal_info.name", ""))
                
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
                logger.warning("Could not find expected form elements on Indeed")
                return False
                
        except Exception as e:
            logger.error(f"Error during Indeed application: {e}")
            return False 