#!/usr/bin/env python3
import json
import logging
import os
import sys
import time
from datetime import datetime
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import job board modules
from job_boards.linkedin import LinkedInBoard
from job_boards.indeed import IndeedBoard
from job_boards.builtin import BuiltInBoard
from job_boards.wellfound import WellFoundBoard
from job_boards.ziprecruiter import ZipRecruiterBoard
from job_boards.welcome_to_the_jungle import WelcomeToTheJungleBoard
from job_boards.base import JobBoardBase
# Add LeverBoard and BaseBoard if you have them
try:
    from job_boards.lever import LeverBoard
except ImportError:
    LeverBoard = None
try:
    from job_boards.base_board import BaseBoard
except ImportError:
    BaseBoard = None

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_application.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.json file."""
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
    with open(config_path) as f:
        config = json.load(f)
    # Replace environment variables in config
    def replace_env_vars(obj):
        if isinstance(obj, dict):
            return {k: replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            return os.getenv(env_var, "")
        return obj
    return replace_env_vars(config)

def setup_webdriver(config):
    """Set up and configure Chrome WebDriver to use existing profile."""
    chrome_options = Options()
    
    # Configure options for using existing Chrome profile
    user_data_dir = config.get("browser_settings", {}).get("chrome_profile_path")
    
    if not user_data_dir:
        # Default locations for Chrome user data directory
        if sys.platform == "win32":
            user_data_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
        elif sys.platform == "darwin":  # macOS
            user_data_dir = os.path.join(os.environ["HOME"], "Library", "Application Support", "Google", "Chrome")
        else:  # Linux
            user_data_dir = os.path.join(os.environ["HOME"], ".config", "google-chrome")
    
    logger.info(f"Using Chrome profile from: {user_data_dir}")
    
    # Add the user-data-dir option to use existing Chrome profile
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")  # Use default profile
    
    # Prevent "Chrome is being controlled by automated test software" notification
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Anti-detection settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Add additional options
    if config.get("headless", False):
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    # Custom user agent to avoid detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Create webdriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        logger.info("WebDriver initialized successfully with existing Chrome profile.")
        return driver
    except Exception as e:
        logger.error(f"Error initializing WebDriver: {str(e)}")
        return None

def process_job_board(board_name, board_class, config, driver):
    """Process a single job board."""
    logger.info(f"Processing {board_name}")
    
    try:
        # Initialize job board with shared driver
        board = board_class(config, driver)
        
        # Login to job board
        login_result = board.login()
        
        if login_result is True:
            logger.info(f"Successfully logged in to {board_name}")
            
            # Get job preferences from config
            job_prefs = config.get('job_preferences', {})
            keywords = ' '.join(job_prefs.get('titles', ['Software Engineer']))
            locations = job_prefs.get('locations', ['Remote'])
            
            # Search for jobs
            for location in locations:
                jobs = board.search_jobs(keywords, location)
                logger.info(f"Found {len(jobs)} jobs on {board_name} for {location}")
                
                # TODO: Filter jobs based on preferences
                
                # TODO: Apply to filtered jobs
                
        elif login_result == "captcha":
            logger.warning(f"CAPTCHA detected on {board_name}. Manual intervention may be required.")
        else:
            logger.error(f"Failed to login to {board_name}")
            
    except Exception as e:
        logger.error(f"Error processing {board_name}: {str(e)}")

def main():
    """Main function to run the job scraper."""
    parser = argparse.ArgumentParser(description="Automated job application script")
    parser.add_argument("--board", help="Specific job board to use", default=None)
    parser.add_argument("--profile", help="Chrome profile path", default=None)
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # If profile path is provided via command line, update config
    if args.profile:
        if "browser_settings" not in config:
            config["browser_settings"] = {}
        config["browser_settings"]["chrome_profile_path"] = args.profile
        config["browser_settings"]["use_existing_profile"] = True
    
    # Check for required directories
    for directory in ['resumes', 'cover_letters']:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"Created directory: {directory}")
    
    # Set up shared Chrome WebDriver
    driver = setup_webdriver(config)
    if not driver:
        logger.error("Failed to initialize WebDriver. Exiting.")
        return
    
    try:
        # Initialize job boards
        boards = {
            "linkedin": LinkedInBoard(config),
            "indeed": IndeedBoard(config),
            "builtin": BuiltInBoard(config),
            "wellfound": WellFoundBoard(config),
            "ziprecruiter": ZipRecruiterBoard(config),
            "welcome_to_the_jungle": WelcomeToTheJungleBoard(config)
        }
        if LeverBoard:
            boards["lever"] = LeverBoard(config)
        if BaseBoard:
            boards["base"] = BaseBoard(config)
        
        # Run specific board or all enabled boards
        if args.board:
            if args.board not in boards:
                logger.error(f"Unknown job board: {args.board}")
                return
            boards_to_run = [args.board]
        else:
            boards_to_run = [name for name, board in boards.items() if config["job_boards"].get(name, {}).get("enabled", False)]
        
        # Process each job board
        for board_name in boards_to_run:
            process_job_board(board_name, boards[board_name], config, driver)
        
        logger.info("Job scraping completed")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
    finally:
        # Close the shared driver
        if driver:
            logger.info("Closing WebDriver.")
            driver.quit()

if __name__ == "__main__":
    main()