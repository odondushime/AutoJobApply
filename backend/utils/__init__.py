"""
Utilities Package
Contains helper functions and utility classes.
"""

from typing import Dict, List, Optional, Union

def safe_get(data: Dict, key: str, default: Optional[Union[str, List, Dict]] = None) -> Optional[Union[str, List, Dict]]:
    """Safely get a value from a dictionary with a default fallback."""
    return data.get(key, default)

def format_score(score: float) -> str:
    """Format a score as a percentage string."""
    return f"{score:.1f}%"

__all__ = ['safe_get', 'format_score']
