"""
Cover letter generator using OpenAI API
"""
import os
import json
from pathlib import Path
import logging
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_template():
    """Load the cover letter template"""
    template_path = Path("cover_letters/cover_letter.txt")
    if not template_path.exists():
        raise FileNotFoundError("Cover letter template not found")
    
    with open(template_path) as f:
        return f.read()

def load_config():
    """Load personal information from config"""
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
    
    with open(config_path) as f:
        return json.load(f)

def generate_cover_letter(job_title, company_name, job_description=""):
    """Generate a personalized cover letter using OpenAI"""
    try:
        # Load template and config
        template = load_template()
        config = load_config()
        personal_info = config["personal_info"]
        
        # Prepare the prompt for OpenAI
        prompt = f"""
        Please help me write a cover letter for a {job_title} position at {company_name}.
        
        My information:
        - Name: {personal_info['name']}
        - Experience: {personal_info['years_of_experience']} years
        - Education: {personal_info['education']}
        - Location: {personal_info['location']}
        
        Job Description:
        {job_description}
        
        Please use this template structure but personalize it for this specific role:
        {template}
        
        Make sure to:
        1. Keep it professional and concise
        2. Highlight relevant skills and experience
        3. Show enthusiasm for the specific role and company
        4. Include specific achievements or responsibilities
        5. Maintain a confident but humble tone
        """
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Generate cover letter
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        cover_letter = response.choices[0].message.content
        
        # Save the generated cover letter
        output_dir = Path("cover_letters/generated")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{company_name.lower().replace(' ', '_')}_cover_letter.txt"
        with open(output_file, "w") as f:
            f.write(cover_letter)
        
        logger.info(f"Cover letter generated and saved to {output_file}")
        return cover_letter
        
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    job_title = "Software Engineer"
    company_name = "Example Company"
    job_description = """
    We are looking for a Software Engineer to join our team. The ideal candidate should have:
    - 3+ years of experience in software development
    - Strong knowledge of Python and JavaScript
    - Experience with React and Django
    - Good understanding of databases and API design
    """
    
    cover_letter = generate_cover_letter(job_title, company_name, job_description)
    if cover_letter:
        print("\nGenerated Cover Letter:")
        print(cover_letter) 