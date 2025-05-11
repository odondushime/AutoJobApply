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
        """Login to direct company sites"""
        # Most company sites don't require login for job searching
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs on direct company websites"""
        jobs = []
        
        # Define company-specific search logic
        companies = {
            "google": {
                "url": "https://careers.google.com/jobs/results/?distance=50&q=software",
                "job_selector": "li.lLd3Je",
                "title_selector": "h2.QJPWVe",
                "location_selector": "span.r0wTof",
                "link_selector": "a.WpHeLc",
                "company_name": "Google"
            },
            "amazon": {
                "url": "https://www.amazon.jobs/en/search?base_query=software&loc_query=United+States",
                "job_selector": "div.job-tile",
                "title_selector": "h3.job-title",
                "location_selector": "p.location-and-id",
                "link_selector": "a.job-link",
                "company_name": "Amazon"
            },
            "microsoft": {
                "url": "https://careers.microsoft.com/us/en/search-results?keywords=software",
                "job_selector": "div.job-card",
                "title_selector": "h2.job-title",
                "location_selector": "span.job-location",
                "link_selector": "a.job-link",
                "company_name": "Microsoft"
            },
            "stripe": {
                "url": "https://stripe.com/jobs/search?q=software",
                "job_selector": "div.job-card",
                "title_selector": "h3.job-title",
                "location_selector": "span.job-location",
                "link_selector": "a.job-link",
                "company_name": "Stripe"
            },
            "gitlab": {
                "url": "https://about.gitlab.com/jobs/all-jobs/",
                "job_selector": "div.job-card",
                "title_selector": "h3.job-title",
                "location_selector": "span.job-location",
                "link_selector": "a.job-link",
                "company_name": "GitLab"
            }
        }
        
        for company_key, company_data in companies.items():
            try:
                logger.info(f"Searching jobs at {company_key}")
                self.driver.get(company_data["url"])
                
                # Check for CAPTCHA
                if self._handle_captcha():
                    continue
                
                time.sleep(5)  # Wait for page to load
                
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, company_data["job_selector"])
                
                for job_element in job_elements[:5]:  # Limit to 5 jobs per company to avoid overloading
                    try:
                        title_elem = job_element.find_element(By.CSS_SELECTOR, company_data["title_selector"])
                        location_elem = job_element.find_element(By.CSS_SELECTOR, company_data["location_selector"])
                        link_elem = job_element.find_element(By.CSS_SELECTOR, company_data["link_selector"])
                        
                        job_data = {
                            "job_title": title_elem.text.strip(),
                            "company": company_data["company_name"],
                            "location": location_elem.text.strip(),
                            "url": link_elem.get_attribute("href"),
                            "job_board": f"{self.board_name}_{company_key}"
                        }
                        job_data["job_id"] = self._get_unique_job_id(job_data)
                        jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing {company_key} job: {e}")
            except Exception as e:
                logger.error(f"Error searching {company_key} jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on a direct company site"""
        try:
            self.driver.get(job_data["url"])
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Wait for and click Apply button
            apply_button = self._wait_for_clickable(
                By.CSS_SELECTOR, 
                "button[type='submit'], button.apply-button, a.apply-button"
            )
            if not apply_button:
                return False
            apply_button.click()
            
            # Wait for application form
            time.sleep(2)
            
            # Fill out application form
            try:
                # Fill name if required
                name_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='name'], input[name='fullName']")
                if name_field:
                    name_field.send_keys(self._get_config_value("personal_info.name", ""))
                
                # Fill email if required
                email_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='email'], input[type='email']")
                if email_field:
                    email_field.send_keys(self._get_config_value("personal_info.email", ""))
                
                # Fill phone if required
                phone_field = self._wait_for_element(By.CSS_SELECTOR, "input[name='phone'], input[name='telephone']")
                if phone_field:
                    phone_field.send_keys(self._get_config_value("personal_info.phone", ""))
                
                # Upload resume if required
                resume_upload = self._wait_for_element(By.CSS_SELECTOR, "input[type='file']")
                if resume_upload:
                    resume_upload.send_keys(str(self.resume_path.absolute()))
                
                # Submit application
                submit_button = self._wait_for_clickable(
                    By.CSS_SELECTOR,
                    "button[type='submit'], button.submit-button, input[type='submit']"
                )
                if submit_button:
                    submit_button.click()
                    time.sleep(3)
                    return True
                
            except NoSuchElementException:
                logger.warning("Could not find expected form elements")
                return False
                
        except Exception as e:
            logger.error(f"Error during direct company application: {e}")
            return False 