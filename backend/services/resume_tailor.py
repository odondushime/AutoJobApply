from typing import Dict, List, Tuple
import re
from dataclasses import dataclass
from .ats_analyzer import ATSAnalyzer

@dataclass
class JobRequirement:
    category: str
    keywords: List[str]
    importance: float  # 0.0 to 1.0

class ResumeTailor:
    def __init__(self):
        self.ats_analyzer = ATSAnalyzer()
        self.requirement_categories = {
            'technical_skills': ['python', 'javascript', 'java', 'c++', 'sql', 'react', 'node.js', 'aws', 'docker', 'kubernetes'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'time management'],
            'education': ['bachelor', 'master', 'phd', 'degree', 'university', 'college'],
            'experience': ['experience', 'years', 'worked', 'developed', 'implemented', 'managed']
        }

    def extract_job_requirements(self, job_description: str) -> List[JobRequirement]:
        """Extract requirements from job description and categorize them."""
        requirements = []
        job_desc_lower = job_description.lower()

        # Extract technical skills
        tech_skills = []
        for skill in self.requirement_categories['technical_skills']:
            if skill in job_desc_lower:
                tech_skills.append(skill)
        if tech_skills:
            requirements.append(JobRequirement('technical_skills', tech_skills, 0.8))

        # Extract soft skills
        soft_skills = []
        for skill in self.requirement_categories['soft_skills']:
            if skill in job_desc_lower:
                soft_skills.append(skill)
        if soft_skills:
            requirements.append(JobRequirement('soft_skills', soft_skills, 0.6))

        # Extract education requirements
        education = []
        for edu in self.requirement_categories['education']:
            if edu in job_desc_lower:
                education.append(edu)
        if education:
            requirements.append(JobRequirement('education', education, 0.7))

        # Extract experience requirements
        experience = []
        for exp in self.requirement_categories['experience']:
            if exp in job_desc_lower:
                experience.append(exp)
        if experience:
            requirements.append(JobRequirement('experience', experience, 0.9))

        return requirements

    def analyze_resume_match(self, resume_text: str, requirements: List[JobRequirement]) -> Dict:
        """Analyze how well the resume matches the job requirements."""
        matches = {}
        resume_lower = resume_text.lower()

        for req in requirements:
            matched_keywords = [kw for kw in req.keywords if kw in resume_lower]
            match_percentage = len(matched_keywords) / len(req.keywords) if req.keywords else 0
            matches[req.category] = {
                'matched_keywords': matched_keywords,
                'missing_keywords': [kw for kw in req.keywords if kw not in resume_lower],
                'match_percentage': match_percentage,
                'importance': req.importance
            }

        return matches

    def generate_tailoring_suggestions(self, matches: Dict) -> List[str]:
        """Generate specific suggestions for tailoring the resume."""
        suggestions = []
        
        for category, match_data in matches.items():
            if match_data['match_percentage'] < 0.8:  # If less than 80% match
                missing = match_data['missing_keywords']
                if missing:
                    suggestions.append(
                        f"Consider adding these {category.replace('_', ' ')}: {', '.join(missing)}"
                    )

        return suggestions

    def tailor_resume(self, resume_text: str, job_description: str) -> Dict:
        """Main function to tailor a resume for a specific job."""
        # Extract requirements from job description
        requirements = self.extract_job_requirements(job_description)
        
        # Analyze how well the resume matches
        matches = self.analyze_resume_match(resume_text, requirements)
        
        # Generate suggestions
        suggestions = self.generate_tailoring_suggestions(matches)
        
        # Calculate overall match score
        overall_score = sum(
            match_data['match_percentage'] * match_data['importance']
            for match_data in matches.values()
        ) / len(matches) if matches else 0
        
        # Ensure ATS score stays high
        ats_score = self.ats_analyzer.calculate_score(
            self.ats_analyzer.analyze_keywords(resume_text),
            self.ats_analyzer.check_formatting(resume_text)
        )
        
        return {
            'overall_match_score': round(overall_score * 100, 2),
            'ats_score': ats_score,
            'matches': matches,
            'suggestions': suggestions,
            'is_ats_compliant': ats_score >= 80
        }

    def get_optimized_resume(self, original_resume: str, job_description: str) -> Tuple[str, Dict]:
        """Generate an optimized version of the resume for the job."""
        # First, get the tailoring analysis
        analysis = self.tailor_resume(original_resume, job_description)
        
        # If ATS score is already good and match is high, return original
        if analysis['ats_score'] >= 80 and analysis['overall_match_score'] >= 80:
            return original_resume, analysis
        
        # Otherwise, generate optimized version
        optimized_resume = original_resume
        
        # Add missing important keywords while maintaining ATS score
        for category, match_data in analysis['matches'].items():
            if match_data['match_percentage'] < 0.8:
                for keyword in match_data['missing_keywords']:
                    # Add keyword in a way that maintains ATS score
                    # This is a simplified version - in reality, you'd want to be more sophisticated
                    if category == 'technical_skills':
                        optimized_resume += f"\n• Proficient in {keyword}"
                    elif category == 'soft_skills':
                        optimized_resume += f"\n• Strong {keyword} abilities"
        
        # Recalculate ATS score for the optimized version
        new_ats_score = self.ats_analyzer.calculate_score(
            self.ats_analyzer.analyze_keywords(optimized_resume),
            self.ats_analyzer.check_formatting(optimized_resume)
        )
        
        # Update analysis with new ATS score
        analysis['optimized_ats_score'] = new_ats_score
        analysis['is_ats_compliant'] = new_ats_score >= 80
        
        return optimized_resume, analysis 