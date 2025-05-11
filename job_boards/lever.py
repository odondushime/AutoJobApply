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
        # Most Lever instances don't require login for job searching
        return True
    
    def search_jobs(self, keywords, location):
        """Search for jobs across companies using Lever"""
        jobs = []
        
        # Get list of companies from config or use defaults
        lever_companies = self._get_config_value("job_search.lever_companies", [
            {"name": "Netflix", "url": "https://jobs.lever.co/netflix"},
            {"name": "Slack", "url": "https://jobs.lever.co/slack"},
            {"name": "Figma", "url": "https://jobs.lever.co/figma"},
            {"name": "Notion", "url": "https://jobs.lever.co/notion"},
            {"name": "Atlassian", "url": "https://jobs.lever.co/atlassian"}
        ])
        
        # Get search keywords from config
        search_keywords = self._get_config_value("job_search.keywords", ["developer", "engineer", "software"])
        exclude_keywords = self._get_config_value("job_search.exclude_keywords", ["senior", "lead", "principal"])
        
        for company in lever_companies:
            try:
                logger.info(f"Searching {company['name']} jobs on Lever")
                self.driver.get(company["url"])
                
                # Check for CAPTCHA
                if self._handle_captcha():
                    continue
                
                # Wait for page to load
                time.sleep(3)
                
                # Try to use search box if available
                search_box = self._wait_for_element(By.CSS_SELECTOR, "input[type='text']")
                if search_box:
                    search_terms = " ".join(search_keywords)
                    search_box.clear()
                    search_box.send_keys(search_terms)
                    search_button = self._wait_for_clickable(By.CSS_SELECTOR, "button[type='submit']")
                    if search_button:
                        search_button.click()
                        time.sleep(3)
                
                # Find all job postings
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.posting")
                
                for job in job_cards[:10]:  # Limit to 10 jobs per company
                    try:
                        title_elem = job.find_element(By.CSS_SELECTOR, "h5")
                        location_elem = job.find_element(By.CSS_SELECTOR, "span.sort-by-location")
                        link_elem = job.find_element(By.CSS_SELECTOR, "a.posting-title")
                        
                        job_title = title_elem.text.strip()
                        
                        # Skip senior/lead positions
                        if any(keyword.lower() in job_title.lower() for keyword in exclude_keywords):
                            logger.info(f"Skipping senior/lead position: {job_title}")
                            continue
                        
                        # Skip jobs that don't match our keywords
                        if not any(keyword.lower() in job_title.lower() for keyword in search_keywords):
                            continue
                        
                        job_data = {
                            "job_title": job_title,
                            "company": company["name"],
                            "location": location_elem.text.strip(),
                            "url": link_elem.get_attribute("href"),
                            "job_board": f"{self.board_name}_{company['name'].lower()}"
                        }
                        job_data["job_id"] = self._get_unique_job_id(job_data)
                        jobs.append(job_data)
                        
                    except NoSuchElementException:
                        continue
                    except Exception as e:
                        logger.error(f"Error parsing {company['name']} job: {e}")
            
            except Exception as e:
                logger.error(f"Error searching {company['name']} jobs: {e}")
        
        return jobs
    
    def apply_to_job(self, job_data):
        """Apply to a job on Lever"""
        try:
            logger.info(f"Applying to {job_data['company']} - {job_data['job_title']}")
            self.driver.get(job_data["url"])
            
            # Check for CAPTCHA
            if self._handle_captcha():
                return False
            
            # Try different apply button selectors
            apply_selectors = [
                "a.postings-btn", 
                "button.postings-btn",
                "a.apply-button",
                "button.apply-button"
            ]
            
            apply_button = None
            for selector in apply_selectors:
                apply_button = self._wait_for_clickable(By.CSS_SELECTOR, selector, timeout=3)
                if apply_button:
                    break
                    
            if not apply_button:
                logger.warning("Could not find apply button")
                return False
                
            apply_button.click()
            
            # Wait for application form
            time.sleep(2)
            
            # Check for redirects to external application systems
            current_url = self.driver.current_url
            if "greenhouse.io" in current_url or "workday.com" in current_url:
                logger.info(f"Redirected to external system: {current_url}")
                return False
            
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
            logger.error(f"Error during Lever application: {e}")
            return False 