"""
LinkedIn job board implementation
"""
import time
import logging
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base import JobBoardBase

logger = logging.getLogger(__name__)

class LinkedInBoard(JobBoardBase):
    """LinkedIn job board implementation"""
    
    @property
    def board_name(self):
        return "linkedin"
    
    def login(self):
        """Login to LinkedIn"""
        try:
            # Get credentials
            email = self.credentials.get("email")
            password = self.credentials.get("password")
            
            if not email or not password:
                logger.error("Missing LinkedIn credentials")
                return False
            
            # Go to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))  # Random delay
            
            # Enter email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(email)
            time.sleep(random.uniform(1, 2))
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            time.sleep(random.uniform(1, 2))
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url:
                logger.info("Successfully logged into LinkedIn")
                return True
            else:
                logger.error("Failed to login to LinkedIn")
                return False
                
        except Exception as e:
            logger.error(f"Error during LinkedIn login: {str(e)}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        try:
            # Construct search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
            self.driver.get(search_url)
            time.sleep(random.uniform(3, 5))
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list"))
            )
            
            # Scroll to load more jobs
            self._scroll_to_load_more_jobs()
            
            # Get all job cards
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
            jobs = []
            
            for card in job_cards:
                try:
                    job = {
                        'title': card.find_element(By.CLASS_NAME, "job-card-list__title").text,
                        'company': card.find_element(By.CLASS_NAME, "job-card-container__company-name").text,
                        'location': card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text,
                        'link': card.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
                    }
                    jobs.append(job)
                except NoSuchElementException:
                    continue
            
            logger.info(f"Found {len(jobs)} jobs on LinkedIn")
            return jobs
            
        except Exception as e:
            logger.error(f"Error searching LinkedIn jobs: {str(e)}")
            return []
    
    def apply_to_job(self, job):
        """Apply to a specific job on LinkedIn"""
        try:
            # Navigate to job page
            self.driver.get(job['link'])
            time.sleep(random.uniform(2, 4))
            
            # Click Easy Apply button if available
            try:
                easy_apply_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
                )
                easy_apply_button.click()
                time.sleep(random.uniform(2, 3))
                
                # Handle the application form
                if self._handle_application_form():
                    logger.info(f"Successfully applied to {job['company']} - {job['title']}")
                    return True
                else:
                    logger.warning(f"Failed to complete application for {job['company']} - {job['title']}")
                    return False
                    
            except TimeoutException:
                logger.info(f"No Easy Apply button found for {job['company']} - {job['title']}")
                return False
                
        except Exception as e:
            logger.error(f"Error applying to job: {str(e)}")
            return False
    
    def _scroll_to_load_more_jobs(self):
        """Scroll down to load more job listings"""
        try:
            # Get the job list container
            job_list = self.driver.find_element(By.CLASS_NAME, "jobs-search-results__list")
            
            # Scroll a few times to load more jobs
            for _ in range(3):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", job_list)
                time.sleep(random.uniform(2, 3))
                
        except Exception as e:
            logger.error(f"Error scrolling job list: {str(e)}")
    
    def _handle_application_form(self):
        """Handle the LinkedIn Easy Apply form"""
        try:
            # Wait for the form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-easy-apply-content"))
            )
            
            # Get personal info from config
            personal_info = self.config.get("personal_info", {})
            
            # Fill out the form fields
            form_fields = {
                "name": ["input[name='name']", "input[name='full_name']", "input[id*='name']"],
                "email": ["input[name='email']", "input[type='email']", "input[id*='email']"],
                "phone": ["input[name='phone']", "input[type='tel']", "input[id*='phone']"],
                "location": ["input[name='location']", "input[id*='location']"],
                "resume": ["input[type='file']", "input[name='resume']", "input[accept='.pdf']"],
                "cover_letter": ["input[name='cover_letter']", "input[name='coverLetter']"]
            }
            
            # Fill each field type
            for field_type, selectors in form_fields.items():
                for selector in selectors:
                    try:
                        field = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        
                        if field_type == "resume":
                            field.send_keys(str(self.resume_path.absolute()))
                            logger.info("Uploaded resume")
                            break
                        elif field_type == "cover_letter" and self.config.get("use_cover_letter", True):
                            field.send_keys(str(self.cover_letter_path.absolute()))
                            logger.info("Uploaded cover letter")
                            break
                        else:
                            value = personal_info.get(field_type, "")
                            if value:
                                field.clear()
                                field.send_keys(value)
                                logger.info(f"Filled {field_type} field")
                                break
                    except TimeoutException:
                        continue
            
            # Handle any additional questions
            self._handle_additional_questions()
            
            # Click Submit button
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
            )
            submit_button.click()
            
            # Wait for confirmation
            time.sleep(random.uniform(2, 3))
            
            # Check for success message
            try:
                success_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-easy-apply-success"))
                )
                logger.info("Application submitted successfully")
                return True
            except TimeoutException:
                logger.warning("No explicit success message found")
                return True  # Still return True as the application might have been submitted
            
        except Exception as e:
            logger.error(f"Error handling application form: {str(e)}")
            return False
    
    def _handle_additional_questions(self):
        """Handle additional questions in the application form"""
        try:
            # Look for common question types
            question_selectors = [
                "input[type='radio']",  # Radio buttons
                "input[type='checkbox']",  # Checkboxes
                "select",  # Dropdowns
                "textarea"  # Text areas
            ]
            
            for selector in question_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        # Get the question text (usually in a nearby label or parent element)
                        question_text = element.get_attribute("aria-label") or element.get_attribute("name")
                        
                        if element.tag_name == "select":
                            # For dropdowns, select the first option
                            element.click()
                            time.sleep(0.5)
                            first_option = element.find_element(By.CSS_SELECTOR, "option:not([value=''])")
                            first_option.click()
                        elif element.get_attribute("type") in ["radio", "checkbox"]:
                            # For radio buttons and checkboxes, click if not selected
                            if not element.is_selected():
                                element.click()
                        elif element.tag_name == "textarea":
                            # For text areas, enter a generic response
                            element.send_keys("I am interested in this position and would be a great fit for the role.")
                        
                        time.sleep(random.uniform(0.5, 1))
                    except Exception as e:
                        logger.warning(f"Error handling question element: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error handling additional questions: {str(e)}") 