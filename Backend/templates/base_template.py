"""Base Template Class for Resume Generation"""

from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from io import BytesIO
from typing import Dict, Any


class BaseTemplate(ABC):
    """Base class for all resume templates"""
    
    def __init__(self, theme_color: str = "#3B82F6"):
        self.theme_color = theme_color
        self.buffer = BytesIO()
    
    def hex_to_rgb(self, hex_color: str):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    
    @abstractmethod
    def generate(self, resume_data: Dict[str, Any]) -> BytesIO:
        """Generate the resume PDF - must be implemented by subclasses"""
        pass
    
    def _get_page_size(self):
        """Override to change page size"""
        return letter
    
    def _get_margins(self):
        """Override to change margins - returns (right, left, top, bottom) in inches"""
        return (0.75, 0.75, 0.75, 0.75)
    
    def create_doc(self):
        """Create document with template-specific settings"""
        margins = self._get_margins()
        return SimpleDocTemplate(
            self.buffer,
            pagesize=self._get_page_size(),
            rightMargin=margins[0]*inch,
            leftMargin=margins[1]*inch,
            topMargin=margins[2]*inch,
            bottomMargin=margins[3]*inch
        )
