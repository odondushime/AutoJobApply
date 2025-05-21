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
import tempfile
import random

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import all job board classes
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

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('job_application.log'),
            logging.StreamHandler()
        ]
    )

def load_config():
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
    """Set up and configure Chrome WebDriver with anti-detection measures"""
    chrome_options = Options()
    
    if config.get("headless", False):
        chrome_options.add_argument("--headless")
        
    # Create a unique temporary directory for Chrome user data
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"user-data-dir={temp_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    
    # Basic options
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # Anti-detection measures
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Randomize user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Additional anti-detection measures
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    # Create webdriver with stealth settings
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            window.chrome = {
                runtime: {}
            };
        """
    })
    
    # Set window size and position randomly
    width = random.randint(1050, 1200)
    height = random.randint(800, 900)
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    driver.set_window_size(width, height)
    driver.set_window_position(x, y)
    
    driver.implicitly_wait(10)
    return driver

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
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Set up WebDriver
        driver = setup_webdriver(config)
        logger.info("WebDriver initialized successfully")
        
        # Process each job board
        for board_name in config["job_boards"]:
            logger.info(f"Processing {board_name}")
            
            # Initialize job board
            board = initialize_job_board(board_name, driver, config)
            if not board:
                logger.error(f"Failed to initialize {board_name}")
                continue
            
            # Login to job board
            if not board.login():
                logger.error(f"Failed to login to {board_name}")
                continue
            
            # Get job search parameters from config
            keywords = config.get("job_search", {}).get("keywords", "software engineer")
            location = config.get("job_search", {}).get("location", "remote")
            
            # Search for jobs
            jobs = board.search_jobs(keywords, location)
            logger.info(f"Found {len(jobs)} jobs on {board_name}")
            
            # Apply to each job
            for job in jobs:
                logger.info(f"Attempting to apply to: {job['company']} - {job['title']}")
                if board.apply_to_job(job):
                    logger.info(f"Successfully applied to {job['company']} - {job['title']}")
                else:
                    logger.warning(f"Failed to apply to {job['company']} - {job['title']}")
                time.sleep(random.uniform(2, 4))  # Random delay between applications
        
        # Keep the browser open
        input("Press Enter to close the browser...")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()