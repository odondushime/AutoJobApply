"""
JobAutoApply - Automated Job Application Script with AI Integration
Supports software developer and tech sales jobs, including Grand Rapids, MI
"""
import os
import time
import json
import random
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import requests
from tqdm import tqdm
from fpdf import FPDF  # You'll need to install this: pip install fpdf

from job_boards import (
    IndeedBoard, LinkedInBoard, BuiltInBoard, WellFoundBoard,
    ZipRecruiterBoard, WelcomeToTheJungleBoard, DirectCompanyBoard
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jobautoapply.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class JobAutoApply:
    """Main class for automated job applications with AI support"""
    
    def __init__(self, config_file="config.json"):
        self.config = self._load_config(config_file)
        self.driver = self._setup_webdriver()
        self.applications_db = self._load_applications_db()
        self.applied_job_ids = set(self.applications_db["job_id"]) if not self.applications_db.empty else set()
        
        # Initialize job boards
        self.job_boards = {
            "indeed": IndeedBoard(self.config, self.driver),
            "linkedin": LinkedInBoard(self.config, self.driver),
            "builtin": BuiltInBoard(self.config, self.driver),
            "wellfound": WellFoundBoard(self.config, self.driver),
            "ziprecruiter": ZipRecruiterBoard(self.config, self.driver),
            "welcome_to_the_jungle": WelcomeToTheJungleBoard(self.config, self.driver),
            "direct_company": DirectCompanyBoard(self.config, self.driver)
        }
        
        # AI API key handling
        self.ai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.ai_api_key:
            logger.warning("OPENAI_API_KEY not set. AI features disabled.")
        
        logger.info("JobAutoApply initialized successfully.")
    
    def _load_config(self, config_file):
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found. Creating default configuration.")
            return self._create_default_config(config_file)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {config_file}. Creating default configuration.")
            return self._create_default_config(f"{config_file}.default")
    
    def _create_default_config(self, config_file):
        """Create default configuration file"""
        default_config = {
            "job_search": {
                "keywords": [
                    "Software Developer",
                    "Software Engineer",
                    "Backend Developer",
                    "Frontend Developer",
                    "Full Stack Developer",
                    "Web Developer",
                    "Application Developer",
                    "Cloud Engineer",
                    "API Developer"
                ],
                "location": "Remote",
                "min_salary": 80000,  # Minimum salary requirement
                "exclude_keywords": [
                    "Senior",
                    "Principal",
                    "Lead",
                    "Architect",
                    "Manager"
                ]
            },
            "credentials": {
                "indeed": {"email": "", "password": ""},
                "linkedin": {"email": "", "password": ""},
                "wellfound": {"email": "", "password": ""},
                "repvue": {"email": "", "password": ""},
                "hired": {"email": "", "password": ""}
            },
            "enabled_job_boards": [
                "indeed", "linkedin", "builtin", "wellfound",
                "repvue", "hired", "lever", "greenhouse"
            ],
            "resume_path": "resumes/resume.pdf",
            "cover_letter_path": "cover_letters/cover_letter.pdf",
            "use_cover_letter": True,
            "apply_limit_per_day": 50,
            "blacklisted_companies": [],
            "auto_generate_cover_letter": True,
            "headless": False,
            "application_delay": {
                "min_seconds": 3,
                "max_seconds": 7
            },
            "browser_settings": {
                "use_existing_profile": False,
                "chrome_profile_path": ""
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        logger.info(f"Created default configuration at {config_file}")
        return default_config
    
    def _setup_webdriver(self):
        """Set up and configure Chrome WebDriver"""
        chrome_options = Options()
        
        if self.config.get("headless", False):
            chrome_options.add_argument("--headless")
            
        # Use existing Chrome profile
        if self.config.get("browser_settings", {}).get("use_existing_profile", False):
            chrome_profile_path = str(Path(self.config["browser_settings"]["chrome_profile_path"]).expanduser().resolve())
            chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
            chrome_options.add_argument("--profile-directory=Default")
            
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        logger.info("WebDriver initialized.")
        return driver
    
    def _load_applications_db(self):
        """Load or create the applications database"""
        db_path = Path("applications_db.csv")
        if db_path.exists():
            return pd.read_csv(db_path)
        
        # Create new database with proper columns
        db = pd.DataFrame(columns=[
            "job_id", "job_title", "company", "location",
            "job_board", "application_date", "status", "url",
            "salary_range", "job_type"  # Added new columns
        ])
        db.to_csv(db_path, index=False)
        logger.info("Created new applications database.")
        return db
    
    def save_cover_letter_as_pdf(self, content, filepath):
        """Convert cover letter text to PDF format"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split content into lines that fit the page width
        # FPDF uses mm for dimensions, roughly 190mm width available
        lines = content.split('\n')
        for line in lines:
            # Handle long lines by wrapping
            pdf.multi_cell(0, 10, line)
        
        pdf.output(filepath)
        return filepath

    def generate_cover_letter(self, job_title, company, job_description=""):
        """Generate a cover letter dynamically using AI API."""
        if not self.ai_api_key:
            logger.warning("AI API key missing. Cannot generate cover letter.")
            return None
        
        try:
            prompt = (
                f"Write a professional cover letter for a {job_title} position at {company}. "
                f"Highlight relevant skills, problem-solving abilities, and teamwork. "
                f"Keep it concise and enthusiastic. "
                f"Use keywords from the job description to tailor the cover letter."
            )
            
            if job_description:
                prompt += f"\n\nJob description: {job_description}"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.ai_api_key}"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a professional cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500
            }
            
            logger.info(f"Generating cover letter for {company}")
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
            
            response_data = response.json()
            if "choices" not in response_data or not response_data["choices"]:
                logger.error("Invalid API response format")
                return None
            
            cover_letter = response_data["choices"][0]["message"]["content"]
            return cover_letter
            
        except requests.exceptions.Timeout:
            logger.error("OpenAI API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            return None

    def apply_to_jobs(self):
        """Main loop to find and apply to jobs."""
        applied_today = 0
        apply_limit = self.config.get("apply_limit_per_day", 50)
        
        # Pause for manual login if using existing profile
        if self.config.get("browser_settings", {}).get("use_existing_profile", False):
            input("\n[Manual Login] Please log in to the job board in the opened browser window. Press Enter here when you are finished logging in and ready to start applying to jobs...\n")
        
        # Login to all enabled job boards
        for board_name in self.config.get("enabled_job_boards", []):
            if board_name in self.job_boards:
                # Skip login if using existing profile
                if self.config.get("browser_settings", {}).get("use_existing_profile", False):
                    logger.info(f"Using existing profile for {board_name}, skipping login")
                    continue
                if not self.job_boards[board_name].login():
                    logger.warning(f"Failed to login to {board_name}")
                    continue
        
        # Search and apply to jobs from each board
        for board_name in self.config.get("enabled_job_boards", []):
            if board_name not in self.job_boards:
                continue
                
            if applied_today >= apply_limit:
                break
                
            board = self.job_boards[board_name]
            keywords = self.config["job_search"]["keywords"]
            location = self.config["job_search"]["location"]
            
            # Search for jobs
            jobs = board.search_jobs(keywords, location)
            
            for job in tqdm(jobs, desc=f"Processing {board_name} jobs"):
                if applied_today >= apply_limit:
                    break
                    
                if job["job_id"] in self.applied_job_ids:
                    logger.info(f"Already applied to {job['company']} - {job['job_title']}")
                    continue
                    
                if job["company"] in self.config.get("blacklisted_companies", []):
                    logger.info(f"Skipping blacklisted company: {job['company']}")
                    continue
                
                # Check for excluded keywords in job title
                if any(keyword.lower() in job["job_title"].lower() 
                      for keyword in self.config["job_search"]["exclude_keywords"]):
                    logger.info(f"Skipping senior/lead position: {job['job_title']}")
                    continue
                
                # Generate cover letter if needed
                if self.config.get("use_cover_letter", True) and self.config.get("auto_generate_cover_letter", True):
                    if cover_letter := self.generate_cover_letter(job["job_title"], job["company"]):
                        # Save generated cover letter
                        cover_letter_dir = Path("cover_letters")
                        cover_letter_dir.mkdir(exist_ok=True)
                        temp_cover_letter_path = cover_letter_dir / f"{job['company']}_{datetime.now().strftime('%Y%m%d')}.pdf"
                        with open(temp_cover_letter_path, "w") as f:
                            f.write(cover_letter)
                        logger.info(f"Generated cover letter saved to {temp_cover_letter_path}")
                
                # Apply to job
                if self.apply_to_job(job):
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_application = {
                        "job_id": job["job_id"],
                        "job_title": job["job_title"],
                        "company": job["company"],
                        "location": job["location"],
                        "job_board": job["job_board"],
                        "application_date": now,
                        "status": "applied",
                        "url": job["url"],
                        "salary_range": job.get("salary_range", "Not specified"),
                        "job_type": job.get("job_type", "Not specified")
                    }
                    
                    self.applications_db.loc[len(self.applications_db)] = new_application
                    self.applications_db.to_csv("applications_db.csv", index=False)
                    self.applied_job_ids.add(job["job_id"])
                    applied_today += 1
                    
                    # Alert user about successful application
                    logger.info(f"""
                    Successfully applied to:
                    Title: {job['job_title']}
                    Company: {job['company']}
                    Location: {job['location']}
                    Job Board: {job['job_board']}
                    URL: {job['url']}
                    Date: {now}
                    """)
                    
                    # Random delay between applications
                    delay_min = self.config.get("application_delay", {}).get("min_seconds", 3)
                    delay_max = self.config.get("application_delay", {}).get("max_seconds", 7)
                    sleep_time = random.uniform(delay_min, delay_max)
                    logger.info(f"Waiting {sleep_time:.2f} seconds before next application")
                    time.sleep(sleep_time)
        
        logger.info(f"Finished applying to {applied_today} jobs today.")

    def apply_to_job(self, job):
        try:
            result = board.apply_to_job(job)
            if result:
                logger.info(f"Successfully applied to {job['company']} - {job['job_title']}")
                return True
            else:
                logger.warning(f"Failed to apply to {job['company']} - {job['job_title']}")
                return False
        except Exception as e:
            logger.error(f"Error applying to {job['company']} - {job['job_title']}: {str(e)}")
            return False

    def quit(self):
        """Properly close browser driver."""
        if hasattr(self, 'driver') and self.driver:
            logger.info("Quitting WebDriver.")
            self.driver.quit()


if __name__ == "__main__":
    try:
        app = JobAutoApply()
        app.apply_to_jobs()
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        # Make sure to quit the driver
        if 'app' in locals():
            app.quit()