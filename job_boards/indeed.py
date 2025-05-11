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
        """Login to Indeed using Google account"""
        if not self.credentials.get("email") or not self.credentials.get("password"):
            logger.warning("No Indeed credentials found")
            return False
        
        try:
            self.driver.get("https://www.indeed.com/login")
            time.sleep(5)  # Wait for page to load
            
            # Click on Google login button
            google_login_button = self._wait_for_clickable(By.CSS_SELECTOR, "button.google-login-button")
            if not google_login_button:
                return False
            google_login_button.click()
            
            # Wait for Google login page
            time.sleep(5)
            
            # Fill in Google email
            google_email_field = self._wait_for_element(By.CSS_SELECTOR, "input[type='email']")
            if not google_email_field:
                return False
            google_email_field.send_keys(self.credentials["email"])
            
            # Click next
            next_button = self._wait_for_clickable(By.CSS_SELECTOR, "button.next-button")
            if not next_button:
                return False
            next_button.click()
            
            # Wait for password field
            time.sleep(5)
            
            # Fill in Google password
            google_password_field = self._wait_for_element(By.CSS_SELECTOR, "input[type='password']")
            if not google_password_field:
                return False
            google_password_field.send_keys(self.credentials["password"])
            
            # Click sign in
            signin_button = self._wait_for_clickable(By.CSS_SELECTOR, "button.signin-button")
            if not signin_button:
                return False
            signin_button.click()
            
            # Wait for successful login
            time.sleep(5)
            return "Sign Out" in self.driver.page_source
            
        except Exception as e:
            logger.error(f"Error logging in to Indeed: {e}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Indeed"""
        jobs = []
        try:
            # Build search URL
            search_url = f"https://www.indeed.com/jobs?q={keywords}&l={location}"
            self.driver.get(search_url)
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            
            for job in job_cards:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                    company_elem = job.find_element(By.CSS_SELECTOR, "span.companyName")
                    location_elem = job.find_element(By.CSS_SELECTOR, "div.companyLocation")
                    
                    job_data = {
                        "job_title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip(),
                        "url": title_elem.get_attribute("href"),
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
                logger.warning("Could not find expected form elements on Indeed")
                return False
                
        except Exception as e:
            logger.error(f"Error during Indeed application: {e}")
            return False 