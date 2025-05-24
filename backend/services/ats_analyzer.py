import re
from typing import Dict, List, Tuple
import PyPDF2
import docx
import io

class ATSAnalyzer:
    def __init__(self):
        self.common_keywords = {
            'technical': ['python', 'javascript', 'java', 'c++', 'sql', 'react', 'node.js', 'aws', 'docker', 'kubernetes'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'time management'],
            'education': ['bachelor', 'master', 'phd', 'degree', 'university', 'college'],
            'experience': ['experience', 'years', 'worked', 'developed', 'implemented', 'managed']
        }

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.lower()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, file_content: bytes) -> str:
        try:
            docx_file = io.BytesIO(file_content)
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.lower()
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def analyze_keywords(self, text: str) -> Dict[str, List[str]]:
        found_keywords = {}
        for category, keywords in self.common_keywords.items():
            found = [keyword for keyword in keywords if keyword in text]
            if found:
                found_keywords[category] = found
        return found_keywords

    def check_formatting(self, text: str) -> List[str]:
        issues = []
        
        # Check for bullet points
        if not re.search(r'[•\-\*]', text):
            issues.append("No bullet points found")
        
        # Check for section headers
        if not re.search(r'(experience|education|skills|work|employment)', text):
            issues.append("Missing common section headers")
        
        # Check for contact information
        if not re.search(r'(email|phone|address|@)', text):
            issues.append("Missing contact information")
        
        return issues

    def calculate_score(self, found_keywords: Dict[str, List[str]], formatting_issues: List[str]) -> int:
        # Base score
        score = 70
        
        # Add points for found keywords
        keyword_score = sum(len(keywords) for keywords in found_keywords.values())
        score += min(keyword_score * 2, 20)  # Max 20 points for keywords
        
        # Subtract points for formatting issues
        score -= len(formatting_issues) * 5
        
        return max(min(score, 100), 0)  # Ensure score is between 0 and 100

    def analyze_resume(self, file_content: bytes, file_type: str) -> Dict:
        # Extract text based on file type
        if file_type == 'pdf':
            text = self.extract_text_from_pdf(file_content)
        elif file_type in ['doc', 'docx']:
            text = self.extract_text_from_docx(file_content)
        else:
            return {"error": "Unsupported file type"}

        # Analyze the resume
        found_keywords = self.analyze_keywords(text)
        formatting_issues = self.check_formatting(text)
        score = self.calculate_score(found_keywords, formatting_issues)

        return {
            "score": score,
            "found_keywords": found_keywords,
            "formatting_issues": formatting_issues,
            "recommendations": self.generate_recommendations(found_keywords, formatting_issues)
        }

    def generate_recommendations(self, found_keywords: Dict[str, List[str]], formatting_issues: List[str]) -> List[str]:
        recommendations = []
        
        # Keyword recommendations
        for category, keywords in self.common_keywords.items():
            if category not in found_keywords:
                recommendations.append(f"Consider adding {category} keywords to your resume")
        
        # Formatting recommendations
        for issue in formatting_issues:
            if "bullet points" in issue:
                recommendations.append("Use bullet points to highlight your achievements")
            elif "section headers" in issue:
                recommendations.append("Include clear section headers (Experience, Education, Skills)")
            elif "contact information" in issue:
                recommendations.append("Add your contact information")
        
        return recommendations 