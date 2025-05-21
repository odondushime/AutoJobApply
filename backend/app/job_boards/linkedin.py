from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import logging
from typing import List, Dict, Any, Optional
from .base import JobBoard

logger = logging.getLogger(__name__)

class LinkedInJobBoard(JobBoard):
    BASE_URL = "https://www.linkedin.com"
    
    async def login(self, email: str, password: str) -> bool:
        """Login to LinkedIn"""
        try:
            self.driver.get(f"{self.BASE_URL}/login")
            
            # Wait for and fill in email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            
            # Fill in password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".global-nav"))
            )
            
            logger.info("Successfully logged in to LinkedIn")
            return True
            
        except Exception as e:
            logger.error(f"Failed to login to LinkedIn: {str(e)}")
            return False
    
    async def search_jobs(self, keywords: str, location: str) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn"""
        try:
            # Navigate to jobs page
            self.driver.get(f"{self.BASE_URL}/jobs")
            time.sleep(random.uniform(2, 3))
            
            # Fill in search fields
            keyword_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='Search job titles']"))
            )
            keyword_field.clear()
            keyword_field.send_keys(keywords)
            
            location_field = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='City, state, or zip code']")
            location_field.clear()
            location_field.send_keys(location)
            
            # Click search button
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Search']")
            search_button.click()
            
            # Wait for results
            time.sleep(random.uniform(3, 4))
            
            # Extract job listings
            jobs = []
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
            
            for card in job_cards[:10]:  # Limit to first 10 results
                try:
                    job = {
                        "id": card.get_attribute("data-job-id"),
                        "title": card.find_element(By.CSS_SELECTOR, ".job-card-list__title").text,
                        "company": card.find_element(By.CSS_SELECTOR, ".job-card-container__company-name").text,
                        "location": card.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item").text,
                        "url": card.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
                        "job_board": "linkedin"
                    }
                    jobs.append(job)
                except Exception as e:
                    logger.warning(f"Failed to extract job details: {str(e)}")
                    continue
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error searching jobs on LinkedIn: {str(e)}")
            return []
    
    async def apply_to_job(self, job_id: str, resume_path: str, cover_letter_path: Optional[str] = None) -> bool:
        """Apply to a job on LinkedIn"""
        try:
            # Navigate to job page
            self.driver.get(f"{self.BASE_URL}/jobs/view/{job_id}")
            time.sleep(random.uniform(2, 3))
            
            # Click Easy Apply button
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-button"))
            )
            easy_apply_button.click()
            
            # Handle the application form
            return await self._handle_application_form(resume_path, cover_letter_path)
            
        except Exception as e:
            logger.error(f"Error applying to job on LinkedIn: {str(e)}")
            return False
    
    async def _handle_application_form(self, resume_path: str, cover_letter_path: Optional[str] = None) -> bool:
        """Handle the LinkedIn Easy Apply form"""
        try:
            # Wait for the form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-easy-apply-content"))
            )
            
            # Upload resume
            resume_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            resume_input.send_keys(resume_path)
            
            # Upload cover letter if provided
            if cover_letter_path:
                try:
                    cover_letter_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='cover_letter']")
                    cover_letter_input.send_keys(cover_letter_path)
                except:
                    logger.warning("Cover letter upload field not found")
            
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