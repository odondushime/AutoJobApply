"""
Welcome to the Jungle job board implementation
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class WelcomeToTheJungleBoard(JobBoardBase):
    """Welcome to the Jungle job board implementation"""
    
    @property
    def board_name(self):
        return "welcome_to_the_jungle"
    
    def login(self):
        """Login to Welcome to the Jungle"""
        try:
            self.driver.get("https://www.welcometothejungle.com/fr/signin")
            time.sleep(2)
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Fill in email
            email_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='email']")
            if not email_field:
                logger.error("Could not find email field")
                return False
            email_field.send_keys(self.credentials.get("email", ""))
            
            # Fill in password
            password_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='password']")
            if not password_field:
                logger.error("Could not find password field")
                return False
            password_field.send_keys(self.credentials.get("password", ""))
            
            # Click sign in
            sign_in_button = self._wait_for_clickable(By.CSS_SELECTOR, "button[type='submit']")
            if not sign_in_button:
                logger.error("Could not find sign in button")
                return False
            sign_in_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "profile" in self.driver.current_url:
                logger.info("Successfully logged in to Welcome to the Jungle")
                return True
            else:
                logger.error("Login failed - not redirected to profile")
                return False
                
        except Exception as e:
            logger.error(f"Error during Welcome to the Jungle login: {e}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs on Welcome to the Jungle"""
        jobs = []
        try:
            # Format keywords for URL
            if isinstance(keywords, list):
                keyword_str = "+".join(keywords)
            else:
                keyword_str = keywords.replace(" ", "+")
            
            # Format location for URL
            location_str = location.replace(" ", "+") if location else "remote"
            
            # Build search URL with filters
            search_url = f"https://www.welcometothejungle.com/fr/jobs?q={keyword_str}&location={location_str}"
            
            # Add filters from config
            filters = []
            if self._get_config_value("job_search.remote_only", False):
                filters.append("workplace_type=remote")
            if self._get_config_value("job_search.experience_level", "entry"):
                filters.append("experience_level=entry")
            
            if filters:
                search_url += "&" + "&".join(filters)
            
            logger.info(f"Searching Welcome to the Jungle with URL: {search_url}")
            self.driver.get(search_url)
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return jobs
            
            # Wait for job listings to load
            time.sleep(5)
            
            # Get exclude keywords from config
            exclude_keywords = self._get_config_value("job_search.exclude_keywords", ["senior", "lead", "principal"])
            
            # Find all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.sc-1pe7b5t-0")
            
            for job in job_cards[:20]:  # Limit to 20 jobs
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "h3.sc-1pe7b5t-3")
                    company_elem = job.find_element(By.CSS_SELECTOR, "span.sc-1pe7b5t-4")
                    location_elem = job.find_element(By.CSS_SELECTOR, "span.sc-1pe7b5t-5")
                    link_elem = job.find_element(By.CSS_SELECTOR, "a.sc-1pe7b5t-1")
                    
                    job_title = title_elem.text.strip()
                    
                    # Skip senior/lead positions
                    if any(keyword.lower() in job_title.lower() for keyword in exclude_keywords):
                        logger.info(f"Skipping senior/lead position: {job_title}")
                        continue
                    
                    job_data = {
                        "job_title": job_title,
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
                    logger.error(f"Error parsing Welcome to the Jungle job: {e}")
            
        except Exception as e:
            logger.error(f"Error searching Welcome to the Jungle jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Welcome to the Jungle"""
        try:
            logger.info(f"Applying to {job_data['company']} - {job_data['job_title']}")
            self.driver.get(job_data["url"])
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button.sc-1pe7b5t-6"
            )
            if not apply_button:
                logger.warning("Could not find apply button")
                return False
            apply_button.click()
            
            # Wait for application form
            time.sleep(2)
            
            # Get personal info from config
            name = self._get_config_value("personal_info.name", "")
            email = self._get_config_value("personal_info.email", "")
            phone = self._get_config_value("personal_info.phone", "")
            
            # Fill out application form
            form_filled = False
            
            # Try to fill name fields
            for name_selector in ["input[name='name']", "input[name='full_name']", "input[id*='name']"]:
                name_field = self._wait_for_element(By.CSS_SELECTOR, name_selector, timeout=2)
                if name_field:
                    name_field.clear()
                    name_field.send_keys(name)
                    form_filled = True
                    break
            
            # Try to fill email fields
            for email_selector in ["input[name='email']", "input[type='email']", "input[id*='email']"]:
                email_field = self._wait_for_element(By.CSS_SELECTOR, email_selector, timeout=2)
                if email_field:
                    email_field.clear()
                    email_field.send_keys(email)
                    form_filled = True
                    break
            
            # Try to fill phone fields
            for phone_selector in ["input[name='phone']", "input[type='tel']", "input[id*='phone']"]:
                phone_field = self._wait_for_element(By.CSS_SELECTOR, phone_selector, timeout=2)
                if phone_field:
                    phone_field.clear()
                    phone_field.send_keys(phone)
                    form_filled = True
                    break
            
            # Upload resume
            for resume_selector in ["input[type='file']", "input[name='resume']", "input[accept='.pdf']"]:
                resume_upload = self._wait_for_element(By.CSS_SELECTOR, resume_selector, timeout=2)
                if resume_upload:
                    resume_upload.send_keys(str(self.resume_path.absolute()))
                    form_filled = True
                    logger.info("Uploaded resume")
                    break
            
            # Upload cover letter if configured
            if self._get_config_value("use_cover_letter", True):
                for cl_selector in ["input[name='cover_letter']", "input[name='coverLetter']", 
                                  "input[type='file']:not([name='resume'])"]:
                    cl_upload = self._wait_for_element(By.CSS_SELECTOR, cl_selector, timeout=2)
                    if cl_upload:
                        cl_upload.send_keys(str(self.cover_letter_path.absolute()))
                        logger.info("Uploaded cover letter")
                        break
            
            if not form_filled:
                logger.warning("Could not fill out any form fields")
                return False
            
            # Try to submit the form
            for submit_selector in ["button[type='submit']", "input[type='submit']", 
                                  "button.submit-app-btn", "button:contains('Submit')"]:
                submit_button = self._wait_for_clickable(By.CSS_SELECTOR, submit_selector, timeout=2)
                if submit_button:
                    submit_button.click()
                    time.sleep(5)
                    
                    # Check for confirmation
                    confirmation_texts = ["thank you", "application received", "application submitted"]
                    page_text = self.driver.page_source.lower()
                    
                    for text in confirmation_texts:
                        if text in page_text:
                            logger.info(f"Application confirmed: '{text}' found on page")
                            return True
                    
                    logger.info("Form submitted, no explicit confirmation found")
                    return True
            
            logger.warning("Could not find submit button")
            return False
                
        except Exception as e:
            logger.error(f"Error during Welcome to the Jungle application: {e}")
            return False 