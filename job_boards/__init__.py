"""
Job board implementations package
"""
from .indeed import IndeedBoard
from .linkedin import LinkedInBoard
from .builtin import BuiltInBoard
from .wellfound import WellFoundBoard
from .ziprecruiter import ZipRecruiterBoard
from .welcome_to_the_jungle import WelcomeToTheJungleBoard
from .direct_company import DirectCompanyBoard

__all__ = [
    'IndeedBoard',
    'LinkedInBoard',
    'BuiltInBoard',
    'WellFoundBoard',
    'ZipRecruiterBoard',
    'WelcomeToTheJungleBoard',
    'DirectCompanyBoard'
] 